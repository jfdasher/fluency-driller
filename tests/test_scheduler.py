"""Scheduler tests — SM-2 due-based selection (replaces MVP ordering)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from drill.server import db, importer
from drill.server.scheduler import next_question, select_next
from drill.server.srs import SrsConfig

UTC = UTC
BASE = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
GOOD_LAT = 25000  # hesitation 25000-250=24750 > 20000 → GOOD under recalibrated defaults
# Constants the mechanics tests were authored against (EASY → 4d); pin them so
# tuning changes to SrsConfig defaults don't churn the due-based selection math.
LEGACY_CFG = SrsConfig(starting_ease=2.5, easy_interval_days=4.0, easy_bonus=1.3)


def _q(ext: str, grader: str = "python", topic: str = "t") -> dict:
    return {
        "external_id": ext,
        "topic": topic,
        "grader": grader,
        "modality": "code",
        "prompt": f"prompt {ext}",
        "canonical_answer": "def solve():\n    return 1",
        "hints": ["h0", "h1"],
        "test_cases": [{"name": "test_a", "source": "def test_a():\n    assert solve() == 1"}],
    }


def _seed(conn, *exts, grader="python", topic="t"):
    importer.import_questions(conn, [_q(e, grader=grader, topic=topic) for e in exts])
    return {q.external_id: q.id for q in db.all_questions(conn)}


def _log(conn, user, qid, verdict, hints_shown=0, ts=None, latency_ms=1000):
    """Insert a submission event, optionally with an explicit timestamp."""
    if ts is None:
        db.append_submission_event(
            conn,
            session_key=None,
            user=user,
            question_id=qid,
            verdict=verdict,
            hint_index=None,
            hints_shown=hints_shown,
            latency_ms=latency_ms,
            answer_text="x",
            judge_comment=None,
            demonstrates_idiom=None,
            judge_json=None,
        )
    else:
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "INSERT INTO events"
            " (event_type, user, question_id, ts, verdict, hints_shown, latency_ms, answer_text)"
            " VALUES ('submission', ?, ?, ?, ?, ?, ?, ?)",
            (user, qid, ts_str, verdict, hints_shown, latency_ms, "x"),
        )
        conn.commit()


# ---------------------------------------------------------------------------
# Basic / edge cases
# ---------------------------------------------------------------------------


def test_empty_db_returns_none(conn):
    assert next_question(conn, "jim", now=BASE) is None


def test_new_card_served_when_nothing_is_due(conn):
    ids = _seed(conn, "a", "b", "c")
    q = next_question(conn, "jim", now=BASE)
    assert q.id == ids["a"]  # lowest ID new card


def test_passed_card_returns_when_due(conn):
    ids = _seed(conn, "a")
    # Pass 'a' at BASE with fast answer (EASY) → interval = 4 days
    _log(conn, "jim", ids["a"], "pass", ts=BASE, latency_ms=1000)
    # Before due: nothing due, no new cards → None
    assert next_question(conn, "jim", now=BASE + timedelta(days=2), cfg=LEGACY_CFG) is None
    # After due: 'a' is overdue → serve it
    q = next_question(conn, "jim", now=BASE + timedelta(days=5), cfg=LEGACY_CFG)
    assert q.id == ids["a"]


def test_most_overdue_card_served_first(conn):
    ids = _seed(conn, "a", "b")
    # Graduate both cards first (two GOODs each)
    t = BASE - timedelta(days=20)
    _log(conn, "jim", ids["a"], "pass", ts=t, latency_ms=GOOD_LAT)  # GOOD step 0→1
    _log(
        conn, "jim", ids["a"], "pass", ts=t + timedelta(minutes=10), latency_ms=GOOD_LAT
    )  # graduate
    _log(
        conn, "jim", ids["b"], "pass", ts=t + timedelta(minutes=20), latency_ms=GOOD_LAT
    )  # GOOD step 0→1
    _log(
        conn, "jim", ids["b"], "pass", ts=t + timedelta(minutes=30), latency_ms=GOOD_LAT
    )  # graduate
    # Then review both: 'a' reviewed 10 days ago, 'b' 5 days ago — 'a' more overdue
    t_review_a = BASE - timedelta(days=10)
    t_review_b = BASE - timedelta(days=5)
    _log(conn, "jim", ids["a"], "pass", ts=t_review_a, latency_ms=GOOD_LAT)  # GOOD review
    _log(conn, "jim", ids["b"], "pass", ts=t_review_b, latency_ms=GOOD_LAT)  # GOOD review
    # Both are overdue; 'a' has earlier due_at → served first
    q = next_question(conn, "jim", now=BASE)
    assert q.id == ids["a"]


def test_failed_card_not_served_within_learning_step(conn):
    ids = _seed(conn, "a", "b")
    # Fail 'a' at BASE; learning step 0 = 1 min → not due until BASE+1min
    _log(conn, "jim", ids["a"], "fail", ts=BASE)
    # 30s later: 'a' not due; 'b' is NEW → serve 'b'
    q = next_question(conn, "jim", now=BASE + timedelta(seconds=30))
    assert q.id == ids["b"]


def test_caught_up_returns_none(conn):
    ids = _seed(conn, "a")
    # Pass 'a' fast (EASY) → interval = 4 days, due at BASE+4d
    _log(conn, "jim", ids["a"], "pass", ts=BASE, latency_ms=1000)
    # No new cards, nothing due yet at BASE+1d
    assert next_question(conn, "jim", now=BASE + timedelta(days=1)) is None


def test_new_card_preferred_over_future_due(conn):
    """NEW cards are introduced when nothing is overdue."""
    ids = _seed(conn, "a", "b")
    # Pass 'a' fast → EASY, interval 4d, due BASE+4d
    _log(conn, "jim", ids["a"], "pass", ts=BASE, latency_ms=1000)
    # 'b' is NEW; at BASE+1d nothing is due → serve 'b'
    q = next_question(conn, "jim", now=BASE + timedelta(days=1))
    assert q.id == ids["b"]


def test_pass_is_per_user(conn):
    ids = _seed(conn, "a")
    # jim passes 'a' 5 days ago → in REVIEW, due 1 day ago (overdue)
    _log(conn, "jim", ids["a"], "pass", ts=BASE - timedelta(days=5), latency_ms=GOOD_LAT)
    _log(
        conn,
        "jim",
        ids["a"],
        "pass",
        ts=BASE - timedelta(days=5) + timedelta(minutes=10),
        latency_ms=GOOD_LAT,
    )
    # kate has no events → 'a' is NEW for kate
    assert next_question(conn, "kate", now=BASE).id == ids["a"]
    # jim gets 'a' back as a review
    assert next_question(conn, "jim", now=BASE).id == ids["a"]


# ---------------------------------------------------------------------------
# Filter tests (grader, topic, topic_keyword) — logic unchanged
# ---------------------------------------------------------------------------


def test_grader_filter(conn):
    _seed(conn, "py1", grader="python")
    ids = _seed(conn, "go1", grader="go")
    q = next_question(conn, "jim", grader="go", now=BASE)
    assert q.id == ids["go1"]
    assert q.grader == "go"


def test_next_question_topic_filter(conn):
    _seed(conn, "a", topic="iteration/sorting")
    ids = _seed(conn, "b", topic="types/dict")
    q = next_question(conn, "jim", topic="types/dict", now=BASE)
    assert q is not None
    assert q.id == ids["b"]


def test_next_question_topic_no_match(conn):
    _seed(conn, "a", topic="iteration/sorting")
    assert next_question(conn, "jim", topic="types/dict", now=BASE) is None


def test_next_filters_by_corpus(conn):
    from drill.server import importer

    importer.import_manifest(conn, "python", [_q("py/1")])
    importer.import_manifest(conn, "pandas", [_q("pd/1")])
    q = next_question(conn, "u", corpus="pandas")
    assert q.external_id == "pd/1" and q.corpus == "pandas"
    q2 = next_question(conn, "u", corpus="python")
    assert q2.external_id == "py/1"


def test_topic_keyword_partial_match(conn):
    ids = _seed(conn, "a", topic="iteration/sorting")
    _seed(conn, "b", topic="types/dict")
    q = next_question(conn, "jim", topic_keyword="iteration", now=BASE)
    assert q is not None
    assert q.id == ids["a"]


def test_topic_keyword_matches_anywhere_in_topic(conn):
    ids = _seed(conn, "a", topic="iteration/sorting")
    q = next_question(conn, "jim", topic_keyword="sorting", now=BASE)
    assert q is not None
    assert q.id == ids["a"]


def test_topic_keyword_no_match_returns_none(conn):
    _seed(conn, "a", topic="iteration/sorting")
    assert next_question(conn, "jim", topic_keyword="heapq", now=BASE) is None


def test_topic_keyword_does_not_affect_exact_topic_filter(conn):
    ids = _seed(conn, "a", topic="types/dict")
    _seed(conn, "b", topic="types/list")
    q = next_question(conn, "jim", topic="types/dict", now=BASE)
    assert q is not None
    assert q.id == ids["a"]


# ---------------------------------------------------------------------------
# select_next — picked card plus available-now counts (due + new snapshot)
# ---------------------------------------------------------------------------


def test_select_next_counts_empty_db(conn):
    sel = select_next(conn, "jim", now=BASE)
    assert sel.question is None
    assert sel.due_count == 0
    assert sel.new_count == 0


def test_select_next_counts_all_new(conn):
    ids = _seed(conn, "a", "b", "c")
    sel = select_next(conn, "jim", now=BASE)
    assert sel.question.id == ids["a"]
    assert sel.due_count == 0
    assert sel.new_count == 3


def test_select_next_counts_mixed_due_and_new(conn):
    ids = _seed(conn, "a", "b", "c")
    # Graduate 'a' then review it overdue so it is due at BASE; 'b'/'c' stay NEW.
    t = BASE - timedelta(days=20)
    _log(conn, "jim", ids["a"], "pass", ts=t, latency_ms=GOOD_LAT)
    _log(conn, "jim", ids["a"], "pass", ts=t + timedelta(minutes=10), latency_ms=GOOD_LAT)
    _log(conn, "jim", ids["a"], "pass", ts=BASE - timedelta(days=10), latency_ms=GOOD_LAT)
    sel = select_next(conn, "jim", now=BASE)
    assert sel.question.id == ids["a"]  # due card preferred
    assert sel.due_count == 1
    assert sel.new_count == 2


def test_select_next_counts_exclude_future_due(conn):
    ids = _seed(conn, "a")
    # Pass 'a' fast → due 4 days out; at BASE+1d it is neither due nor new.
    _log(conn, "jim", ids["a"], "pass", ts=BASE, latency_ms=1000)
    sel = select_next(conn, "jim", now=BASE + timedelta(days=1))
    assert sel.question is None
    assert sel.due_count == 0
    assert sel.new_count == 0


def test_inactive_question_is_not_scheduled(conn):
    """Inactive questions (active=0) should never be returned by next_question()."""
    from tests.conftest import SAMPLE_QUESTION

    importer.import_questions(conn, [SAMPLE_QUESTION])
    conn.execute("UPDATE questions SET active = 0 WHERE id = 1")
    conn.commit()
    result = next_question(conn, user="jim", now=BASE)
    assert result is None


# ---------------------------------------------------------------------------
# Unified event stream — soon / bury override tests
# ---------------------------------------------------------------------------


def _override(conn, user, qid, kind, ts):
    ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO events (event_type, user, question_id, ts) VALUES (?, ?, ?, ?)",
        (kind, user, qid, ts_str),
    )
    conn.commit()


def test_buried_card_drops_out_of_due_set(conn):
    ids = _seed(conn, "a", "b")
    # Make 'a' due now via a fast pass long ago, then bury it.
    _log(conn, "jim", ids["a"], "pass", ts=BASE - timedelta(days=10), latency_ms=1000)
    _override(conn, "jim", ids["a"], "bury", BASE - timedelta(days=1))
    sel = select_next(conn, "jim", now=BASE)
    # bury pushes 'a' far into the future (> now), so only 'b' (NEW) is due.
    assert sel.question.external_id == "b"


def test_soon_card_becomes_due_immediately(conn):
    ids = _seed(conn, "a", "b")
    # 'a' graduates to a FUTURE due date: a fast clean pass → EASY → 4-day interval.
    _log(conn, "jim", ids["a"], "pass", ts=BASE, latency_ms=1000)  # due BASE+4d
    now = BASE + timedelta(days=1)
    # Without 'soon', 'a' is not yet due (+1d < +4d), so the NEW card 'b' is served.
    assert select_next(conn, "jim", now=now).question.external_id == "b"
    # 'soon' at +1d resets 'a' to relearning (due +1 min); just after that, 'a' is due.
    _override(conn, "jim", ids["a"], "soon", now)
    sel = select_next(conn, "jim", now=now + timedelta(minutes=2))
    assert sel.question.external_id == "a"
