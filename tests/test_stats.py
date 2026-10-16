"""Unit tests for stats_* db query functions."""

import pytest

from drill.server import db, importer

from .conftest import SAMPLE_QUESTION


@pytest.fixture
def seeded(conn):
    """conn with one question imported and accessible as (conn, question_id)."""
    importer.import_questions(conn, [SAMPLE_QUESTION])
    qid = conn.execute(
        "SELECT id FROM questions WHERE external_id = ?",
        (SAMPLE_QUESTION["external_id"],),
    ).fetchone()["id"]
    return conn, qid


def _submission(conn, *, session_key, user, question_id, verdict, latency_ms=5000):
    db.append_submission_event(
        conn,
        session_key=session_key,
        user=user,
        question_id=question_id,
        verdict=verdict,
        hint_index=None,
        hints_shown=0,
        latency_ms=latency_ms,
        answer_text="def solve(): pass",
        judge_comment=None,
        demonstrates_idiom=verdict != "fail",
        judge_json=None,
    )


def test_stats_topics_empty(seeded):
    conn, _ = seeded
    result = db.stats_topics(conn, "nobody")
    assert result == []


def test_stats_topics_aggregates_by_topic(seeded):
    conn, qid = seeded
    sk = "s1"
    _submission(conn, session_key=sk, user="jim", question_id=qid, verdict="pass", latency_ms=4000)
    _submission(conn, session_key=sk, user="jim", question_id=qid, verdict="fail", latency_ms=8000)

    rows = db.stats_topics(conn, "jim")
    assert len(rows) == 1
    row = rows[0]
    assert row["topic"] == SAMPLE_QUESTION["topic"]
    assert row["attempts"] == 2
    assert row["pass_count"] == 1
    assert row["fail"] == 1
    assert row["pass_rate"] == 0.5
    assert row["clean_pass_rate"] == 0.5
    assert row["avg_latency_ms"] == 6000


def test_stats_trends_empty(seeded):
    conn, _ = seeded
    assert db.stats_trends(conn, "nobody") == []


def test_stats_trends_groups_by_date(seeded):
    conn, qid = seeded
    sk = "s1"
    _submission(conn, session_key=sk, user="jim", question_id=qid, verdict="pass", latency_ms=3000)
    _submission(conn, session_key=sk, user="jim", question_id=qid, verdict="fail", latency_ms=9000)

    rows = db.stats_trends(conn, "jim", date_range="all")
    assert len(rows) == 1  # both submissions on same day
    assert rows[0]["attempts"] == 2
    assert rows[0]["pass_count"] == 1
    assert rows[0]["pass_rate"] == 0.5


def test_stats_session_winsorizes_latency_outliers(seeded):
    # Two clean passes in one session: one absurd walk-away (10 min) and one
    # normal (100 s). Both avg and median must use the latency clamped to the
    # 5-minute cap (300000 ms), not the raw 600000.
    conn, qid = seeded
    _submission(
        conn, session_key="s1", user="jim", question_id=qid, verdict="pass", latency_ms=600000
    )  # 10 min → clamps to 300000
    _submission(
        conn, session_key="s1", user="jim", question_id=qid, verdict="pass", latency_ms=100000
    )  # 100 s → unchanged

    row = db.stats_session(conn, "s1", "jim")
    # avg of clamped [300000, 100000] = 200000 (raw would be 350000)
    assert row["avg_latency_ms"] == 200000
    # median of clamped [100000, 300000] = (100000 + 300000)//2 = 200000
    assert row["median_latency_ms"] == 200000


def test_stats_cards_empty(seeded):
    conn, _ = seeded
    assert db.stats_cards(conn, "nobody") == []


def test_stats_cards_per_question(seeded):
    conn, qid = seeded
    sk = "s1"
    _submission(conn, session_key=sk, user="jim", question_id=qid, verdict="fail", latency_ms=10000)
    _submission(conn, session_key=sk, user="jim", question_id=qid, verdict="pass", latency_ms=4000)
    db.append_hint_event(conn, session_key=sk, user="jim", question_id=qid, hint_index=0)

    rows = db.stats_cards(conn, "jim")
    assert len(rows) == 1
    card = rows[0]
    assert card["question_id"] == qid
    assert card["attempts"] == 2
    assert card["pass_count"] == 1
    assert card["last_verdict"] == "pass"
    assert card["avg_latency_ms"] == 7000
    assert card["hints_ever"] == 1
    assert card["cheated"] == 0


def test_stats_cards_topic_filter(seeded):
    conn, qid = seeded
    _submission(conn, session_key="s1", user="jim", question_id=qid, verdict="pass")
    # matches topic keyword
    rows = db.stats_cards(conn, "jim", topic="sorting")
    assert len(rows) == 1
    # non-matching keyword
    rows = db.stats_cards(conn, "jim", topic="nonexistent")
    assert len(rows) == 0


def test_stats_coverage_unattempted(seeded):
    conn, _ = seeded
    rows = db.stats_coverage(conn, "nobody")
    assert len(rows) == 1
    row = rows[0]
    assert row["total_questions"] == 1
    assert row["attempted"] == 0
    assert row["coverage_pct"] == 0.0
    assert row["pass_rate"] is None


def test_stats_coverage_after_attempt(seeded):
    conn, qid = seeded
    _submission(conn, session_key="s1", user="jim", question_id=qid, verdict="pass")
    rows = db.stats_coverage(conn, "jim")
    assert len(rows) == 1
    row = rows[0]
    assert row["total_questions"] == 1
    assert row["attempted"] == 1
    assert row["coverage_pct"] == 1.0
    assert row["pass_rate"] == 1.0


def test_coverage_scoped_to_corpus(conn):
    from drill.server import importer

    importer.import_manifest(conn, "python", [{**SAMPLE_QUESTION, "external_id": "py/1"}])
    importer.import_manifest(conn, "pandas", [{**SAMPLE_QUESTION, "external_id": "pd/1"}])
    rows = db.stats_coverage(conn, "u", corpus="pandas")
    total = sum(r["total_questions"] for r in rows)
    assert total == 1  # only the pandas question counted


def test_stats_session_empty(seeded):
    conn, _ = seeded
    result = db.stats_session(conn, "no-key", "anon")
    assert result["questions"] == 0
    assert result["pass_count"] == 0
    assert result["avg_latency_ms"] is None
    assert result["median_latency_ms"] is None


def test_stats_session_counts_correctly(seeded):
    conn, qid = seeded
    sk = "sess-1"
    db.append_question_event(conn, session_key=sk, user="jim", question_id=qid)
    _submission(conn, session_key=sk, user="jim", question_id=qid, verdict="pass", latency_ms=6000)
    db.append_hint_event(conn, session_key=sk, user="jim", question_id=qid, hint_index=0)

    result = db.stats_session(conn, sk, "jim")
    assert result["questions"] == 1
    assert result["pass_count"] == 1
    assert result["pass_hinted"] == 0
    assert result["fail"] == 0
    assert result["hints_used"] == 1
    assert result["cheats"] == 0
    assert result["avg_latency_ms"] == 6000
    assert result["median_latency_ms"] == 6000  # single submission → median == value


# --- stats_day --------------------------------------------------------------


def test_stats_day_empty(seeded):
    conn, _ = seeded
    result = db.stats_day(conn, "nobody")
    assert result["questions"] == 0
    assert result["pass_count"] == 0
    assert result["pass_hinted"] == 0
    assert result["fail"] == 0
    assert result["hints_used"] == 0
    assert result["cheats"] == 0
    assert result["avg_latency_ms"] is None
    assert result["median_latency_ms"] is None
    assert result["date"]  # non-empty string


def test_stats_day_counts_todays_events(seeded):
    conn, qid = seeded
    sk = "day-sess"
    db.append_question_event(conn, session_key=sk, user="jim", question_id=qid)
    _submission(conn, session_key=sk, user="jim", question_id=qid, verdict="pass", latency_ms=6000)
    db.append_hint_event(conn, session_key=sk, user="jim", question_id=qid, hint_index=0)

    result = db.stats_day(conn, "jim")
    assert result["questions"] == 1
    assert result["pass_count"] == 1
    assert result["pass_hinted"] == 0
    assert result["fail"] == 0
    assert result["hints_used"] == 1
    assert result["cheats"] == 0
    assert result["avg_latency_ms"] == 6000
    assert result["median_latency_ms"] == 6000
