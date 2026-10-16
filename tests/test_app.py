"""API tests for /next and /submit (PRD §6, acceptance #2-#4, #7)."""

import pytest
from fastapi.testclient import TestClient

from drill.server import db, importer
from drill.server.app import create_app
from drill.server.judge import Judge, JudgeError, JudgeResult

from .conftest import SAMPLE_QUESTION

PASS = JudgeResult(
    verdict_proposal="pass", demonstrates_idiom=True, hint_index=None, comment="good idiom"
)
FAIL = JudgeResult(
    verdict_proposal="fail", demonstrates_idiom=False, hint_index=None, comment="wrong idiom"
)


class ProgrammableJudge(Judge):
    def __init__(self, result=PASS, error=False):
        self.result = result
        self.error = error

    def judge(self, *, question, answer_text, test_output):
        if self.error:
            raise JudgeError("judge down")
        return self.result


@pytest.fixture
def make_client(tmp_path):
    clients = []

    def _make(judge):
        path = str(tmp_path / "drill.db")
        conn = db.connect(path)
        db.init_db(conn)
        importer.import_questions(conn, [SAMPLE_QUESTION])
        conn.close()
        client = TestClient(create_app(db_path=path, judge=judge))
        clients.append(client)
        return client, path

    yield _make
    for c in clients:
        c.close()


def _submission_count(path: str) -> int:
    conn = db.connect(path)
    try:
        return conn.execute(
            "SELECT COUNT(*) AS c FROM events WHERE event_type = 'submission'"
        ).fetchone()["c"]
    finally:
        conn.close()


def _submit(client, **over):
    body = {
        "user": "jim",
        "question_id": 1,
        "answer_text": "def solve(d):\n    return sorted(d)",
        "test_output": {"passed": 2, "failed": 0, "detail": []},
        "latency_ms": 4200,
        "hints_already_shown": 0,
    }
    body.update(over)
    return client.post("/submit", json=body)


# --- GET /next --------------------------------------------------------------


def test_next_returns_question_without_canonical(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/next", params={"user": "jim"})
    assert r.status_code == 200
    body = r.json()
    assert body["question_id"] == 1
    assert body["entry_point"] == "solve"
    assert body["stub"] == SAMPLE_QUESTION["stub"]
    assert "canonical_answer" not in body
    assert body["hints_total"] == 3


def test_next_includes_hints_total(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/next", params={"user": "jim"})
    assert r.status_code == 200
    assert r.json()["hints_total"] == 3


def test_next_includes_external_id(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/next", params={"user": "jim"})
    assert r.status_code == 200
    assert r.json()["external_id"] == SAMPLE_QUESTION["external_id"]


def test_next_includes_available_counts(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/next", params={"user": "jim"})
    assert r.status_code == 200
    body = r.json()
    # Single seeded question, never attempted → one NEW card available now.
    assert body["due_count"] == 0
    assert body["new_count"] == 1


def test_next_logs_question_event(make_client):
    client, path = make_client(ProgrammableJudge())
    client.get("/next", params={"user": "jim"})
    conn = db.connect(path)
    count = conn.execute(
        "SELECT COUNT(*) AS c FROM events WHERE event_type = 'question'"
    ).fetchone()["c"]
    conn.close()
    assert count == 1


def test_session_key_ties_question_and_submission(make_client):
    client, path = make_client(ProgrammableJudge(FAIL))
    client.get("/next", params={"user": "jim"})
    _submit(client)
    conn = db.connect(path)
    rows = conn.execute("SELECT event_type, session_key FROM events ORDER BY id").fetchall()
    conn.close()
    keys = [r["session_key"] for r in rows]
    assert all(k is not None for k in keys)
    assert len(set(keys)) == 1  # same session key across both events


def test_next_404_when_exhausted(make_client):
    client, _ = make_client(ProgrammableJudge(PASS))
    _submit(client)  # pass the only question
    r = client.get("/next", params={"user": "jim"})
    assert r.status_code == 404
    assert r.json()["detail"] == "nothing due right now"


def test_next_with_topic_query_param(make_client):
    """?topic= matching the only question returns 200."""
    client, _ = make_client(ProgrammableJudge())
    topic = SAMPLE_QUESTION["topic"]
    r = client.get("/next", params={"user": "jim", "topic": topic})
    assert r.status_code == 200
    assert r.json()["question_id"] == 1


def test_next_topic_no_match_returns_404(make_client):
    """?topic= with no matching questions returns 404."""
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/next", params={"user": "jim", "topic": "no-such-topic"})
    assert r.status_code == 404


def test_next_topic_keyword_matches(make_client):
    """GET /next?topic_keyword=sorting returns a question whose topic contains 'sorting'."""
    client, _ = make_client(ProgrammableJudge())
    resp = client.get("/next", params={"user": "jim", "topic_keyword": "sorting"})
    assert resp.status_code == 200
    assert "sorting" in resp.json()["topic"]


def test_next_topic_keyword_no_match_returns_404(make_client):
    """GET /next?topic_keyword=heapq returns 404 when no question topic matches."""
    client, _ = make_client(ProgrammableJudge())
    resp = client.get("/next", params={"user": "jim", "topic_keyword": "heapq"})
    assert resp.status_code == 404


# --- GET /goto ----------------------------------------------------------


def test_goto_by_question_id(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/goto", params={"user": "jim", "question_id": 1})
    assert r.status_code == 200
    body = r.json()
    assert body["question_id"] == 1
    assert body["external_id"] == SAMPLE_QUESTION["external_id"]


def test_goto_by_external_id(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/goto", params={"user": "jim", "external_id": SAMPLE_QUESTION["external_id"]})
    assert r.status_code == 200
    assert r.json()["question_id"] == 1


def test_goto_unknown_question_id_404(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/goto", params={"user": "jim", "question_id": 9999})
    assert r.status_code == 404


def test_goto_unknown_external_id_404(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/goto", params={"user": "jim", "external_id": "nope/nope"})
    assert r.status_code == 404


def test_goto_requires_exactly_one_param(make_client):
    client, _ = make_client(ProgrammableJudge())
    assert client.get("/goto", params={"user": "jim"}).status_code == 400
    r = client.get(
        "/goto",
        params={
            "user": "jim",
            "question_id": 1,
            "external_id": SAMPLE_QUESTION["external_id"],
        },
    )
    assert r.status_code == 400


def test_goto_ignores_active_flag(make_client):
    client, _ = make_client(ProgrammableJudge())
    patch_r = client.patch("/question/1/active", json={"active": False})
    assert patch_r.json()["active"] is False
    r = client.get("/goto", params={"user": "jim", "question_id": 1})
    assert r.status_code == 200
    assert r.json()["question_id"] == 1


def test_goto_logs_question_event_and_sets_session(make_client):
    client, path = make_client(ProgrammableJudge())
    client.get("/goto", params={"user": "jim", "question_id": 1})
    conn = db.connect(path)
    count = conn.execute(
        "SELECT COUNT(*) AS c FROM events WHERE event_type = 'question'"
    ).fetchone()["c"]
    conn.close()
    assert count == 1


def test_goto_enables_hint_without_prior_next(make_client):
    client, _ = make_client(ProgrammableJudge())
    client.get("/goto", params={"user": "jim", "question_id": 1})
    r = client.get("/hint", params={"user": "jim"})
    assert r.status_code == 200


def test_goto_enables_submit_without_prior_next(make_client):
    client, _ = make_client(ProgrammableJudge())
    client.get("/goto", params={"user": "jim", "question_id": 1})
    r = _submit(client)
    assert r.status_code == 200


def test_goto_ambiguous_external_id_without_corpus_409(tmp_path):
    path = str(tmp_path / "drill.db")
    conn = db.connect(path)
    db.init_db(conn)
    importer.import_manifest(
        conn, "python", [{**SAMPLE_QUESTION, "external_id": "a/1", "topic": "py/t"}]
    )
    importer.import_manifest(
        conn, "pandas", [{**SAMPLE_QUESTION, "external_id": "a/1", "topic": "pd/t"}]
    )
    conn.close()
    client = TestClient(create_app(db_path=path, judge=ProgrammableJudge()))
    r = client.get("/goto", params={"user": "u", "external_id": "a/1"})
    assert r.status_code == 409
    client.close()


def test_goto_external_id_with_corpus_resolves_200(tmp_path):
    path = str(tmp_path / "drill.db")
    conn = db.connect(path)
    db.init_db(conn)
    importer.import_manifest(
        conn, "python", [{**SAMPLE_QUESTION, "external_id": "a/1", "topic": "py/t"}]
    )
    importer.import_manifest(
        conn, "pandas", [{**SAMPLE_QUESTION, "external_id": "a/1", "topic": "pd/t"}]
    )
    conn.close()
    client = TestClient(create_app(db_path=path, judge=ProgrammableJudge()))
    r = client.get("/goto", params={"user": "u", "external_id": "a/1", "corpus": "pandas"})
    assert r.status_code == 200
    assert r.json()["topic"] == "pd/t"
    client.close()


def test_nextquestion_preserves_name_source_tests_to_client():
    from drill.server.models import NextQuestion, Question, Test

    q = Question(
        id=1,
        external_id="x",
        topic="t",
        grader="python",
        modality="code",
        prompt="p",
        stub=None,
        entry_point="make",
        canonical_answer="c",
        hints=[],
        test_cases=[Test(name="test_a", source="def test_a():\n    assert make(3)(5) == 15")],
    )
    nq = NextQuestion.from_question(q, due_count=0, new_count=0)
    dumped = nq.model_dump()
    assert dumped["test_cases"][0] == {
        "name": "test_a",
        "source": "def test_a():\n    assert make(3)(5) == 15",
    }


# --- POST /submit -----------------------------------------------------------


def test_submit_pass_logs_one_event(make_client):
    client, path = make_client(ProgrammableJudge(PASS))
    r = _submit(client)
    assert r.status_code == 200
    body = r.json()
    assert body["verdict"] == "pass"
    assert body["hint"] is None
    assert _submission_count(path) == 1


def test_submit_idiom_missing_fails_with_hint(make_client):
    client, _ = make_client(ProgrammableJudge(FAIL))
    body = _submit(client, hints_already_shown=0).json()
    assert body["verdict"] == "fail"
    assert body["hint"] == SAMPLE_QUESTION["hints"][0]
    assert body["hint_index"] == 0


def test_submit_pass_after_hint_is_pass_hinted(make_client):
    client, _ = make_client(ProgrammableJudge(PASS))
    body = _submit(client, hints_already_shown=1).json()
    assert body["verdict"] == "pass_hinted"
    # pass_hinted → HARD → card is in learning step 0 (1 min); not served immediately
    r = client.get("/next", params={"user": "jim"})
    assert r.status_code == 404


def test_judge_index_wins_over_hints_already_shown(make_client):
    j = ProgrammableJudge(
        JudgeResult(verdict_proposal="fail", demonstrates_idiom=False, hint_index=1, comment="x")
    )
    client, _ = make_client(j)
    body = _submit(client, hints_already_shown=0).json()
    assert body["hint_index"] == 1
    assert body["hint"] == SAMPLE_QUESTION["hints"][1]


def test_hint_exhaustion_returns_canonical(make_client):
    client, _ = make_client(ProgrammableJudge(FAIL))
    body = _submit(client, hints_already_shown=3).json()  # 3 hints -> exhausted
    assert body["verdict"] == "fail"
    assert body["hint"] is None
    assert SAMPLE_QUESTION["canonical_answer"] in body["judge_comment"]


def test_judge_unavailable_returns_503_and_logs_nothing(make_client):
    client, path = make_client(ProgrammableJudge(error=True))
    r = _submit(client)
    assert r.status_code == 503
    assert _submission_count(path) == 0


def test_event_records_advisory_signal_and_raw_payload(make_client):
    client, path = make_client(ProgrammableJudge(FAIL))
    _submit(client)
    conn = db.connect(path)
    row = conn.execute(
        "SELECT demonstrates_idiom, judge_json FROM events WHERE event_type = 'submission'"
    ).fetchone()
    conn.close()
    assert row["demonstrates_idiom"] == 0
    assert "verdict_proposal" in row["judge_json"]


def test_submit_response_includes_question_id_and_external_id(make_client):
    client, _ = make_client(ProgrammableJudge())
    client.get("/next", params={"user": "jim"})
    r = _submit(client)
    body = r.json()
    assert body["question_id"] == 1
    assert body["external_id"] == SAMPLE_QUESTION["external_id"]


def test_submit_fail_response_includes_question_id_and_external_id(make_client):
    client, _ = make_client(ProgrammableJudge(FAIL))
    client.get("/next", params={"user": "jim"})
    r = _submit(client)
    body = r.json()
    assert body["question_id"] == 1
    assert body["external_id"] == SAMPLE_QUESTION["external_id"]


def test_submit_unknown_question_404(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = _submit(client, question_id=9999)
    assert r.status_code == 404


# --- GET /hint --------------------------------------------------------------


def test_hint_returns_first_hint_with_position(make_client):
    client, _ = make_client(ProgrammableJudge())
    client.get("/next", params={"user": "jim"})
    r = client.get("/hint", params={"user": "jim"})
    assert r.status_code == 200
    body = r.json()
    assert body["hint"] == SAMPLE_QUESTION["hints"][0]
    assert body["hint_index"] == 0
    assert body["hints_total"] == 3


def test_hint_advances_on_repeated_calls(make_client):
    client, _ = make_client(ProgrammableJudge())
    client.get("/next", params={"user": "jim"})
    client.get("/hint", params={"user": "jim"})
    r = client.get("/hint", params={"user": "jim"})
    body = r.json()
    assert body["hint_index"] == 1
    assert body["hint"] == SAMPLE_QUESTION["hints"][1]


def test_hint_exhausted_returns_null(make_client):
    client, path = make_client(ProgrammableJudge())
    client.get("/next", params={"user": "jim"})
    for _ in range(3):
        client.get("/hint", params={"user": "jim"})
    r = client.get("/hint", params={"user": "jim"})
    body = r.json()
    assert body["hint"] is None
    assert body["hint_index"] is None
    assert body["hints_total"] == 3
    # exhausted call must not log an event
    conn = db.connect(path)
    count = conn.execute("SELECT COUNT(*) AS c FROM events WHERE event_type = 'hint'").fetchone()[
        "c"
    ]
    conn.close()
    assert count == 3


def test_hint_without_session_returns_400(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/hint", params={"user": "jim"})
    assert r.status_code == 400


def test_hint_logs_event(make_client):
    client, path = make_client(ProgrammableJudge())
    client.get("/next", params={"user": "jim"})
    client.get("/hint", params={"user": "jim"})
    conn = db.connect(path)
    count = conn.execute("SELECT COUNT(*) AS c FROM events WHERE event_type = 'hint'").fetchone()[
        "c"
    ]
    conn.close()
    assert count == 1


# --- GET /cheat -------------------------------------------------------------


def test_cheat_returns_canonical_answer(make_client):
    client, _ = make_client(ProgrammableJudge())
    client.get("/next", params={"user": "jim"})
    r = client.get("/cheat", params={"user": "jim"})
    assert r.status_code == 200
    assert r.json()["canonical_answer"] == SAMPLE_QUESTION["canonical_answer"]


def test_cheat_without_session_returns_400(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/cheat", params={"user": "jim"})
    assert r.status_code == 400


def test_cheat_logs_event(make_client):
    client, path = make_client(ProgrammableJudge())
    client.get("/next", params={"user": "jim"})
    client.get("/cheat", params={"user": "jim"})
    conn = db.connect(path)
    count = conn.execute("SELECT COUNT(*) AS c FROM events WHERE event_type = 'cheat'").fetchone()[
        "c"
    ]
    conn.close()
    assert count == 1


def test_session_key_ties_all_event_types(make_client):
    client, path = make_client(ProgrammableJudge(FAIL))
    client.get("/next", params={"user": "jim"})
    client.get("/hint", params={"user": "jim"})
    client.get("/cheat", params={"user": "jim"})
    _submit(client)
    conn = db.connect(path)
    rows = conn.execute("SELECT session_key FROM events ORDER BY id").fetchall()
    conn.close()
    keys = [r["session_key"] for r in rows]
    assert len(set(keys)) == 1
    assert keys[0] is not None


def test_session_key_persists_across_next_calls(make_client):
    client, path = make_client(ProgrammableJudge())
    client.get("/next", params={"user": "jim"})
    client.get("/next", params={"user": "jim"})
    conn = db.connect(path)
    keys = [
        r["session_key"]
        for r in conn.execute(
            "SELECT session_key FROM events WHERE event_type = 'question' ORDER BY id"
        ).fetchall()
    ]
    conn.close()
    assert len(keys) == 2
    assert keys[0] == keys[1], "session_key must persist across /next calls"


def test_statistics_coverage(make_client):
    client, _ = make_client(ProgrammableJudge(PASS))
    # Before any attempts — one question seeded, zero attempted
    r = client.get("/statistics/coverage", params={"user": "jim"})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 1
    assert rows[0]["total_questions"] == 1
    assert rows[0]["attempted"] == 0

    # After a pass
    client.get("/next", params={"user": "jim"})
    _submit(client)
    r = client.get("/statistics/coverage", params={"user": "jim"})
    rows = r.json()
    assert rows[0]["attempted"] == 1
    assert rows[0]["coverage_pct"] == 1.0


def test_statistics_cards(make_client):
    client, _ = make_client(ProgrammableJudge(PASS))
    client.get("/next", params={"user": "jim"})
    _submit(client)
    r = client.get("/statistics/cards", params={"user": "jim"})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 1
    assert rows[0]["question_id"] == 1
    assert rows[0]["pass_count"] == 1
    assert rows[0]["last_verdict"] == "pass"


def test_statistics_trends(make_client):
    client, _ = make_client(ProgrammableJudge(PASS))
    client.get("/next", params={"user": "jim"})
    _submit(client)
    r = client.get("/statistics/trends", params={"user": "jim", "date_range": "all"})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 1
    assert rows[0]["attempts"] == 1
    assert rows[0]["pass_rate"] == 1.0


def test_statistics_topics(make_client):
    client, _ = make_client(ProgrammableJudge(PASS))
    client.get("/next", params={"user": "jim"})
    _submit(client)
    r = client.get("/statistics/topics", params={"user": "jim"})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 1
    assert rows[0]["topic"] == SAMPLE_QUESTION["topic"]
    assert rows[0]["pass_count"] == 1
    assert rows[0]["pass_rate"] == 1.0


def test_statistics_session_no_cookie(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/statistics/session", params={"user": "jim"})
    assert r.status_code == 400


def test_statistics_session_returns_aggregate(make_client):
    client, _ = make_client(ProgrammableJudge(PASS))
    client.get("/next", params={"user": "jim"})
    _submit(client)
    r = client.get("/statistics/session", params={"user": "jim"})
    assert r.status_code == 200
    body = r.json()
    assert body["questions"] == 1
    assert body["pass_count"] == 1
    assert body["fail"] == 0
    assert "session_key" in body


# --- GET /statistics/day ----------------------------------------------------


def test_statistics_day_returns_aggregate(make_client):
    client, _ = make_client(ProgrammableJudge(PASS))
    client.get("/next", params={"user": "jim"})
    _submit(client)
    r = client.get("/statistics/day", params={"user": "jim"})
    assert r.status_code == 200
    body = r.json()
    assert body["questions"] == 1
    assert body["pass_count"] == 1
    assert body["fail"] == 0
    assert "date" in body


def test_statistics_day_empty(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.get("/statistics/day", params={"user": "nobody"})
    assert r.status_code == 200
    body = r.json()
    assert body["questions"] == 0
    assert body["avg_latency_ms"] is None
    assert body["median_latency_ms"] is None


# --- PATCH /question/{id}/active -------------------------------------------


def test_patch_question_active_deactivate(make_client):
    client, path = make_client(ProgrammableJudge())
    r = client.patch("/question/1/active", json={"active": False})
    assert r.status_code == 200
    body = r.json()
    assert body["question_id"] == 1
    assert body["active"] is False
    conn = db.connect(path)
    row = conn.execute("SELECT active FROM questions WHERE id = 1").fetchone()
    conn.close()
    assert row["active"] == 0


def test_patch_question_active_activate(make_client):
    client, _ = make_client(ProgrammableJudge())
    client.patch("/question/1/active", json={"active": False})
    r = client.patch("/question/1/active", json={"active": True})
    assert r.status_code == 200
    assert r.json()["active"] is True


def test_patch_question_active_toggle(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.patch("/question/1/active", json={})
    assert r.status_code == 200
    assert r.json()["active"] is False
    r2 = client.patch("/question/1/active", json={})
    assert r2.json()["active"] is True


def test_patch_question_active_404(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.patch("/question/999/active", json={"active": False})
    assert r.status_code == 404


# --- POST /question/{id}/comment -------------------------------------------


def test_post_question_comment(make_client):
    client, path = make_client(ProgrammableJudge())
    r = client.post("/question/1/comment", json={"user": "jim", "comment": "bad question"})
    assert r.status_code == 200
    body = r.json()
    assert "event_id" in body
    conn = db.connect(path)
    row = conn.execute("SELECT * FROM events WHERE id = ?", (body["event_id"],)).fetchone()
    conn.close()
    assert row["event_type"] == "comment"
    assert row["answer_text"] == "bad question"
    assert row["user"] == "jim"


def test_post_question_comment_404(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.post("/question/999/comment", json={"user": "jim", "comment": "x"})
    assert r.status_code == 404


def _override_count(path: str, kind: str) -> int:
    conn = db.connect(path)
    try:
        return conn.execute(
            "SELECT COUNT(*) AS c FROM events WHERE event_type = ?", (kind,)
        ).fetchone()["c"]
    finally:
        conn.close()


def test_override_soon_appends_event(make_client):
    client, path = make_client(ProgrammableJudge())
    client.get("/next", params={"user": "jim"})  # establish a session cookie
    r = client.post("/override", json={"user": "jim", "question_id": 1, "kind": "soon"})
    assert r.status_code == 200
    body = r.json()
    assert body["kind"] == "soon"
    assert body["question_id"] == 1
    assert _override_count(path, "soon") == 1


def test_override_bury_appends_event(make_client):
    client, path = make_client(ProgrammableJudge())
    r = client.post("/override", json={"user": "jim", "question_id": 1, "kind": "bury"})
    assert r.status_code == 200
    assert _override_count(path, "bury") == 1


def test_override_rejects_bad_kind(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.post("/override", json={"user": "jim", "question_id": 1, "kind": "nope"})
    assert r.status_code == 422


def test_override_unknown_question_404(make_client):
    client, _ = make_client(ProgrammableJudge())
    r = client.post("/override", json={"user": "jim", "question_id": 9999, "kind": "soon"})
    assert r.status_code == 404


def test_hint_count_scoped_to_question(conn):
    import copy

    from drill.server import importer

    from .conftest import SAMPLE_QUESTION

    q2 = copy.deepcopy(SAMPLE_QUESTION)
    q2["external_id"] = "sorting/q2"
    importer.import_questions(conn, [SAMPLE_QUESTION, q2])
    qid1 = conn.execute(
        "SELECT id FROM questions WHERE external_id = ?", (SAMPLE_QUESTION["external_id"],)
    ).fetchone()["id"]
    qid2 = conn.execute("SELECT id FROM questions WHERE external_id = 'sorting/q2'").fetchone()[
        "id"
    ]

    sk = "study-session-1"
    db.append_hint_event(conn, session_key=sk, user="jim", question_id=qid1, hint_index=0)
    db.append_hint_event(conn, session_key=sk, user="jim", question_id=qid1, hint_index=1)
    db.append_hint_event(conn, session_key=sk, user="jim", question_id=qid2, hint_index=0)

    assert db.hint_count_for_session(conn, sk, qid1) == 2
    assert db.hint_count_for_session(conn, sk, qid2) == 1


def test_submit_records_prefill_chars(make_client):
    from drill.content.scaffold import scaffold
    from tests.conftest import SAMPLE_QUESTION

    client, path = make_client(ProgrammableJudge(PASS))
    client.get("/next", params={"user": "jim"})
    _submit(client)
    expected = len(
        scaffold(SAMPLE_QUESTION["prompt"], SAMPLE_QUESTION["stub"], SAMPLE_QUESTION["entry_point"])
    )
    conn = db.connect(path)
    try:
        row = conn.execute(
            "SELECT prefill_chars FROM events WHERE event_type='submission'"
        ).fetchone()
    finally:
        conn.close()
    assert row["prefill_chars"] == expected


def test_submit_returns_grading_block(make_client):
    client, _ = make_client(ProgrammableJudge(PASS))
    client.get("/next", params={"user": "jim"})
    r = _submit(client, latency_ms=1000)
    g = r.json()["grading"]
    assert g["grade"] in {"EASY", "GOOD"}
    assert g["phase"] in {"LEARNING", "REVIEW"}
    assert set(g["counterfactual_days"]) == {"GOOD", "EASY", "HARD"}
    # EASY counterfactual is never sooner than GOOD (easy_bonus >= 1).
    assert g["counterfactual_days"]["EASY"] >= g["counterfactual_days"]["GOOD"]
    assert isinstance(g["rationale"], str) and g["rationale"]
