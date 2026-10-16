"""FastAPI proctor service.

Stateless: every request opens its own SQLite connection. The judge is injected
at construction (env-selected in production, a stub in tests).

Run with either:
    uvicorn --factory drill.server.app:create_app
    uvicorn drill.server.app:app          # lazily built (PEP 562 __getattr__)
"""

from __future__ import annotations

import os
import sqlite3
import uuid
from datetime import UTC, datetime

from fastapi import Depends, FastAPI, HTTPException, Request
from starlette.middleware.sessions import SessionMiddleware

from ..content.scaffold import scaffold
from . import db
from .judge import Judge, JudgeError, JudgeResult, build_judge
from .models import (
    ActivePatch,
    ActiveResponse,
    CardStats,
    CheatResponse,
    CommentRequest,
    CommentResponse,
    CoverageStats,
    DayStats,
    Grading,
    HintResponse,
    NextQuestion,
    OverrideRequest,
    OverrideResponse,
    Question,
    SessionStats,
    SubmitRequest,
    SubmitResponse,
    TopicStats,
    TrendStats,
)
from .scheduler import select_next
from .srs import Grade, SrsConfig, derive_grade, replay, step


def _resolve_verdict(
    result: JudgeResult, question: Question, hints_already_shown: int
) -> SubmitResponse:
    """Map the authoritative ``verdict_proposal`` to a stored verdict + hint.

    pass + no hints  -> pass
    pass + hints     -> pass_hinted
    fail             -> fail, returning the judge's hint_index (if valid) else
                        the hint at hints_already_shown; canonical answer when
                        the ladder is exhausted.
    """
    if result.verdict_proposal == "pass":
        verdict = "pass" if hints_already_shown == 0 else "pass_hinted"
        return SubmitResponse(
            verdict=verdict,
            question_id=question.id,
            external_id=question.external_id,
            judge_comment=result.comment,
        )

    hints = question.hints
    idx = result.hint_index
    if idx is None or not (0 <= idx < len(hints)):
        idx = hints_already_shown
    if 0 <= idx < len(hints):
        return SubmitResponse(
            verdict="fail",
            question_id=question.id,
            external_id=question.external_id,
            hint=hints[idx],
            hint_index=idx,
            judge_comment=result.comment,
        )
    # ladder exhausted: no hint, hand over the canonical answer
    return SubmitResponse(
        verdict="fail",
        question_id=question.id,
        external_id=question.external_id,
        hint=None,
        hint_index=None,
        judge_comment=(
            f"{result.comment}\n\nNo more hints. Canonical answer:\n{question.canonical_answer}"
        ),
    )


def _conn_dep(request: Request):
    conn = db.connect(request.app.state.db_path)
    try:
        yield conn
    finally:
        conn.close()


def _build_grading(conn, user, question_id, *, latency_ms, hints_shown, author_chars, verdict, now):
    """Compute the grade, rationale, projection, and counterfactuals for the
    just-appended submission (the latest event for this user+question)."""
    cfg = SrsConfig()
    events = db.scheduler_events_for_user(conn, user).get(question_id, [])
    if not events:
        return None
    last = events[-1]
    ts = last["ts"]
    state_before = replay(events[:-1], cfg, now)

    grade = derive_grade(verdict, hints_shown, latency_ms, author_chars, cfg)
    actual = step(state_before, grade, ts, cfg)

    def days_until(state):
        return round((state.due_at - ts).total_seconds() / 86400.0, 2)

    counter = {
        g.value: days_until(step(state_before, g, ts, cfg))
        for g in (Grade.GOOD, Grade.EASY, Grade.HARD)
    }

    if verdict == "fail":
        rationale = "failed — does not demonstrate the idiom"
    elif latency_ms is None:
        rationale = f"clean pass, {hints_shown} hints; no timing recorded"
    else:
        budget_s = cfg.ms_per_char * author_chars / 1000.0
        recall_s = latency_ms / 1000.0
        hinted = "hinted" if verdict == "pass_hinted" else "clean"
        rationale = (
            f"recall {recall_s:.1f}s vs {budget_s:.0f}s typing budget "
            f"(+{cfg.hesitation_fast_ms / 1000:.0f}s grace), {hinted}, "
            f"{hints_shown} hints"
        )

    return Grading(
        grade=grade.value,
        rationale=rationale,
        phase=actual.phase,
        surfaced=actual.due_at <= now,
        next_interval_days=days_until(actual),
        next_due=actual.due_at.isoformat(),
        counterfactual_days=counter,
    )


def create_app(db_path: str | None = None, judge: Judge | None = None) -> FastAPI:
    db_path = db_path or os.environ.get("DRILL_DB_PATH", "drill.db")
    judge = judge or build_judge()

    # Ensure the schema exists before serving.
    boot = db.connect(db_path)
    db.init_db(boot)
    boot.close()

    app = FastAPI(title="Fluency Drill Proctor")
    secret = os.environ.get("DRILL_SESSION_SECRET", os.urandom(32).hex())
    app.add_middleware(SessionMiddleware, secret_key=secret)
    app.state.db_path = db_path
    app.state.judge = judge

    @app.get("/next", response_model=NextQuestion)
    def get_next(
        user: str,
        grader: str | None = None,
        topic: str | None = None,
        topic_keyword: str | None = None,
        corpus: str | None = None,
        request: Request = ...,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> NextQuestion:
        sel = select_next(
            conn,
            user,
            grader,
            topic=topic,
            topic_keyword=topic_keyword,
            corpus=corpus,
            now=datetime.now(UTC),
        )
        q = sel.question
        if q is None:
            raise HTTPException(status_code=404, detail="nothing due right now")
        session_key = request.session.get("session_key") or str(uuid.uuid4())
        request.session["session_key"] = session_key
        request.session["question_id"] = q.id
        request.session["user"] = user
        db.append_question_event(conn, session_key=session_key, user=user, question_id=q.id)
        return NextQuestion.from_question(q, due_count=sel.due_count, new_count=sel.new_count)

    @app.get("/goto", response_model=NextQuestion)
    def get_goto(
        user: str,
        question_id: int | None = None,
        external_id: str | None = None,
        corpus: str | None = None,
        request: Request = ...,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> NextQuestion:
        if (question_id is None) == (external_id is None):
            raise HTTPException(
                status_code=400,
                detail="pass exactly one of question_id or external_id",
            )
        try:
            q = (
                db.get_question(conn, question_id)
                if question_id is not None
                else db.get_question_by_external_id(conn, external_id, corpus=corpus)
            )
        except db.AmbiguousExternalId as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        if q is None:
            raise HTTPException(status_code=404, detail="no question matches")
        sel = select_next(conn, user, now=datetime.now(UTC))
        session_key = request.session.get("session_key") or str(uuid.uuid4())
        request.session["session_key"] = session_key
        request.session["question_id"] = q.id
        request.session["user"] = user
        db.append_question_event(conn, session_key=session_key, user=user, question_id=q.id)
        return NextQuestion.from_question(q, due_count=sel.due_count, new_count=sel.new_count)

    @app.get("/hint", response_model=HintResponse)
    def get_hint(
        user: str,
        request: Request,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> HintResponse:
        session_key = request.session.get("session_key")
        question_id = request.session.get("question_id")
        if not session_key or question_id is None:
            raise HTTPException(status_code=400, detail="no active session; call /next first")
        question = db.get_question(conn, question_id)
        if question is None:
            raise HTTPException(status_code=404, detail="unknown question")
        hints = question.hints
        hint_index = db.hint_count_for_session(conn, session_key, question_id)
        if hint_index >= len(hints):
            return HintResponse(hint=None, hint_index=None, hints_total=len(hints))
        db.append_hint_event(
            conn,
            session_key=session_key,
            user=user,
            question_id=question_id,
            hint_index=hint_index,
        )
        return HintResponse(hint=hints[hint_index], hint_index=hint_index, hints_total=len(hints))

    @app.get("/cheat", response_model=CheatResponse)
    def get_cheat(
        user: str,
        request: Request,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> CheatResponse:
        session_key = request.session.get("session_key")
        question_id = request.session.get("question_id")
        if not session_key or question_id is None:
            raise HTTPException(status_code=400, detail="no active session; call /next first")
        question = db.get_question(conn, question_id)
        if question is None:
            raise HTTPException(status_code=404, detail="unknown question")
        db.append_cheat_event(
            conn,
            session_key=session_key,
            user=user,
            question_id=question_id,
        )
        return CheatResponse(canonical_answer=question.canonical_answer)

    @app.post("/submit", response_model=SubmitResponse)
    def post_submit(
        req: SubmitRequest,
        request: Request,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> SubmitResponse:
        question = db.get_question(conn, req.question_id)
        if question is None:
            raise HTTPException(status_code=404, detail="unknown question")

        try:
            result = request.app.state.judge.judge(
                question=question,
                answer_text=req.answer_text,
                test_output=req.test_output,
            )
        except JudgeError:
            # Log nothing to events on judge failure (PRD §6).
            raise HTTPException(status_code=503, detail="judge unavailable; retry") from None

        response = _resolve_verdict(result, question, req.hints_already_shown)

        prefill_chars = len(scaffold(question.prompt, question.stub, question.entry_point))
        session_key = request.session.get("session_key")
        db.append_submission_event(
            conn,
            session_key=session_key,
            user=req.user,
            question_id=question.id,
            verdict=response.verdict,
            hint_index=response.hint_index,
            hints_shown=req.hints_already_shown,
            latency_ms=req.latency_ms,
            answer_text=req.answer_text,
            judge_comment=response.judge_comment,
            demonstrates_idiom=result.demonstrates_idiom,
            judge_json=result.model_dump_json(),
            prefill_chars=prefill_chars,
        )
        author_chars = max(0, len(req.answer_text) - prefill_chars)
        response.grading = _build_grading(
            conn,
            req.user,
            question.id,
            latency_ms=req.latency_ms,
            hints_shown=req.hints_already_shown,
            author_chars=author_chars,
            verdict=response.verdict,
            now=datetime.now(UTC),
        )
        return response

    @app.post("/override", response_model=OverrideResponse)
    def post_override(
        req: OverrideRequest,
        request: Request,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> OverrideResponse:
        if db.get_question(conn, req.question_id) is None:
            raise HTTPException(status_code=404, detail="unknown question")
        session_key = request.session.get("session_key")
        event_id = db.append_override_event(
            conn,
            session_key=session_key,
            user=req.user,
            question_id=req.question_id,
            kind=req.kind,
        )
        return OverrideResponse(question_id=req.question_id, kind=req.kind, event_id=event_id)

    @app.get("/statistics/coverage", response_model=list[CoverageStats])
    def get_statistics_coverage(
        user: str,
        grader: str | None = None,
        corpus: str | None = None,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> list[CoverageStats]:
        rows = db.stats_coverage(conn, user, grader=grader, corpus=corpus)
        return [CoverageStats(**r) for r in rows]

    @app.get("/statistics/cards", response_model=list[CardStats])
    def get_statistics_cards(
        user: str,
        topic: str | None = None,
        date_range: str | None = None,
        date_range_start: str | None = None,
        date_range_end: str | None = None,
        corpus: str | None = None,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> list[CardStats]:
        rows = db.stats_cards(
            conn,
            user,
            topic=topic,
            date_range=date_range,
            date_range_start=date_range_start,
            date_range_end=date_range_end,
            corpus=corpus,
        )
        return [CardStats(**r) for r in rows]

    @app.get("/statistics/trends", response_model=list[TrendStats])
    def get_statistics_trends(
        user: str,
        date_range: str | None = "30days",
        date_range_start: str | None = None,
        date_range_end: str | None = None,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> list[TrendStats]:
        rows = db.stats_trends(
            conn,
            user,
            date_range=date_range,
            date_range_start=date_range_start,
            date_range_end=date_range_end,
        )
        return [TrendStats(**r) for r in rows]

    @app.get("/statistics/topics", response_model=list[TopicStats])
    def get_statistics_topics(
        user: str,
        grader: str | None = None,
        date_range: str | None = None,
        date_range_start: str | None = None,
        date_range_end: str | None = None,
        corpus: str | None = None,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> list[TopicStats]:
        rows = db.stats_topics(
            conn,
            user,
            grader=grader,
            date_range=date_range,
            date_range_start=date_range_start,
            date_range_end=date_range_end,
            corpus=corpus,
        )
        return [TopicStats(**r) for r in rows]

    @app.get("/statistics/session", response_model=SessionStats)
    def get_statistics_session(
        user: str,
        request: Request,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> SessionStats:
        session_key = request.session.get("session_key")
        if not session_key:
            raise HTTPException(status_code=400, detail="no active session; call /next first")
        result = db.stats_session(conn, session_key, user)
        return SessionStats(session_key=session_key, **result)

    @app.get("/statistics/day", response_model=DayStats)
    def get_statistics_day(
        user: str,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> DayStats:
        result = db.stats_day(conn, user)
        return DayStats(**result)

    @app.patch("/question/{question_id}/active", response_model=ActiveResponse)
    def patch_question_active(
        question_id: int,
        body: ActivePatch,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> ActiveResponse:
        new_active = db.set_question_active(conn, question_id, body.active)
        if new_active is None:
            raise HTTPException(status_code=404, detail="Question not found")
        return ActiveResponse(question_id=question_id, active=new_active)

    @app.post("/question/{question_id}/comment", response_model=CommentResponse)
    def post_question_comment(
        question_id: int,
        body: CommentRequest,
        conn: sqlite3.Connection = Depends(_conn_dep),
    ) -> CommentResponse:
        row = conn.execute("SELECT id FROM questions WHERE id = ?", (question_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Question not found")
        event_id = db.append_comment_event(
            conn, user=body.user, question_id=question_id, comment=body.comment
        )
        return CommentResponse(event_id=event_id)

    return app


def __getattr__(name: str):
    # Lazy module-level `app` so importing create_app in tests never constructs
    # a real Anthropic client (PEP 562).
    if name == "app":
        return create_app()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
