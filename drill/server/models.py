"""Pydantic models shared across the proctor service.

Domain models (`Question`, `Test`) and the HTTP request/response shapes for
the API in `app.py`. The judge's own result schema lives in `judge.py`.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

Verdict = Literal["pass", "pass_hinted", "fail"]
Modality = Literal["code", "fill_in"]


class Test(BaseModel):
    """One assert-based test file shipped to the client; `source` defines `def test_*()`."""

    __test__ = False  # not a pytest test class

    name: str
    source: str


class Question(BaseModel):
    """A single atomic, idiom-level drill question."""

    id: int | None = None
    corpus: str = "python"
    external_id: str | None = None
    topic: str
    grader: str
    modality: Modality = "code"
    prompt: str
    stub: str | None = None
    entry_point: str = "solve"
    canonical_answer: str
    hints: list[str] = Field(default_factory=list)
    test_cases: list[Test] = Field(default_factory=list)


# --- API: GET /next ---------------------------------------------------------


class NextQuestion(BaseModel):
    """Payload returned to the client for a fetched question.

    Deliberately omits ``canonical_answer`` — the client never sees it.
    """

    question_id: int
    external_id: str | None
    topic: str
    grader: str
    modality: Modality
    prompt: str
    stub: str | None
    entry_point: str
    test_cases: list[Test]
    hints_total: int
    due_count: int
    new_count: int

    @classmethod
    def from_question(cls, q: Question, *, due_count: int, new_count: int) -> NextQuestion:
        assert q.id is not None
        return cls(
            question_id=q.id,
            external_id=q.external_id,
            topic=q.topic,
            grader=q.grader,
            modality=q.modality,
            prompt=q.prompt,
            stub=q.stub,
            entry_point=q.entry_point,
            test_cases=q.test_cases,
            hints_total=len(q.hints),
            due_count=due_count,
            new_count=new_count,
        )


# --- API: POST /submit ------------------------------------------------------


class TestOutput(BaseModel):
    """Client's self-reported test results (honor system)."""

    __test__ = False  # not a pytest test class

    passed: int = 0
    failed: int = 0
    detail: list[Any] = Field(default_factory=list)


class SubmitRequest(BaseModel):
    user: str
    question_id: int
    answer_text: str
    test_output: TestOutput | None = None
    latency_ms: int | None = None
    hints_already_shown: int = 0


class Grading(BaseModel):
    grade: str
    rationale: str
    phase: str
    surfaced: bool
    next_interval_days: float
    next_due: str
    counterfactual_days: dict[str, float]


class SubmitResponse(BaseModel):
    verdict: Verdict
    question_id: int
    external_id: str | None = None
    hint: str | None = None
    hint_index: int | None = None
    judge_comment: str | None = None
    grading: Grading | None = None


# --- API: GET /hint ---------------------------------------------------------


class HintResponse(BaseModel):
    hint: str | None
    hint_index: int | None
    hints_total: int


# --- API: GET /cheat --------------------------------------------------------


class CheatResponse(BaseModel):
    canonical_answer: str


# --- API: POST /override ----------------------------------------------------


class OverrideRequest(BaseModel):
    user: str
    question_id: int
    kind: Literal["soon", "bury"]


class OverrideResponse(BaseModel):
    question_id: int
    kind: str
    event_id: int


# --- API: PATCH /question/{id}/active / POST /question/{id}/comment ---------


class ActivePatch(BaseModel):
    active: bool | None = None


class ActiveResponse(BaseModel):
    question_id: int
    active: bool


class CommentRequest(BaseModel):
    user: str
    comment: str


class CommentResponse(BaseModel):
    event_id: int


# --- API: GET /statistics/* -------------------------------------------------


class SessionStats(BaseModel):
    session_key: str
    questions: int
    pass_count: int
    pass_hinted: int
    fail: int
    hints_used: int
    cheats: int
    avg_latency_ms: int | None
    median_latency_ms: int | None


class DayStats(BaseModel):
    date: str
    questions: int
    pass_count: int
    pass_hinted: int
    fail: int
    hints_used: int
    cheats: int
    avg_latency_ms: int | None
    median_latency_ms: int | None


class TopicStats(BaseModel):
    topic: str
    attempts: int
    pass_count: int
    pass_hinted: int
    fail: int
    pass_rate: float
    clean_pass_rate: float
    avg_latency_ms: int | None


class TrendStats(BaseModel):
    date: str
    attempts: int
    pass_count: int
    pass_hinted: int
    fail: int
    pass_rate: float
    avg_latency_ms: int | None


class CardStats(BaseModel):
    question_id: int
    external_id: str | None
    topic: str
    attempts: int
    pass_count: int
    last_verdict: Verdict | None
    avg_latency_ms: int | None
    hints_ever: int
    cheated: bool


class CoverageStats(BaseModel):
    topic: str
    total_questions: int
    attempted: int
    coverage_pct: float
    pass_rate: float | None
