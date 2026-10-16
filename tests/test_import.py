import copy
import sqlite3 as _sqlite3

import pytest

from drill.server import db, importer

from .conftest import SAMPLE_QUESTION


def test_import_inserts_question(conn):
    n = importer.import_questions(conn, [SAMPLE_QUESTION])
    assert n == 1

    questions = db.all_questions(conn)
    assert len(questions) == 1
    q = questions[0]
    assert q.external_id == SAMPLE_QUESTION["external_id"]
    assert q.entry_point == "solve"
    assert q.hints == SAMPLE_QUESTION["hints"]
    assert len(q.test_cases) == 2
    assert q.test_cases[0].name == "test_mixed_keys"
    assert "solve(" in q.test_cases[0].source


def test_import_is_idempotent_and_upserts_on_external_id(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])

    edited = copy.deepcopy(SAMPLE_QUESTION)
    edited["prompt"] = "EDITED PROMPT"
    importer.import_questions(conn, [edited])

    questions = db.all_questions(conn)
    assert len(questions) == 1, "re-import on same external_id must not duplicate"
    assert questions[0].prompt == "EDITED PROMPT"


def test_import_requires_external_id(conn):
    bad = {k: v for k, v in SAMPLE_QUESTION.items() if k != "external_id"}
    with pytest.raises(ValueError):
        importer.import_questions(conn, [bad])


def test_entry_point_defaults_to_solve(conn):
    no_ep = {k: v for k, v in SAMPLE_QUESTION.items() if k != "entry_point"}
    importer.import_questions(conn, [no_ep])
    assert db.all_questions(conn)[0].entry_point == "solve"


def test_get_question_roundtrip(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    qid = db.all_questions(conn)[0].id
    q = db.get_question(conn, qid)
    assert q is not None
    assert q.id == qid
    assert q.canonical_answer == SAMPLE_QUESTION["canonical_answer"]
    assert db.get_question(conn, 9999) is None


def test_get_question_by_external_id_roundtrip(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    q = db.get_question_by_external_id(conn, SAMPLE_QUESTION["external_id"])
    assert q is not None
    assert q.external_id == SAMPLE_QUESTION["external_id"]
    assert q.canonical_answer == SAMPLE_QUESTION["canonical_answer"]
    assert db.get_question_by_external_id(conn, "nonexistent/id") is None


def test_get_by_external_id_corpus_scoped(conn):
    importer.import_manifest(conn, "python", [{**SAMPLE_QUESTION, "external_id": "a/1"}])
    importer.import_manifest(conn, "pandas", [{**SAMPLE_QUESTION, "external_id": "a/1"}])
    q = db.get_question_by_external_id(conn, "a/1", corpus="pandas")
    assert q is not None and q.corpus == "pandas"


def test_get_by_external_id_ambiguous_raises(conn):
    importer.import_manifest(conn, "python", [{**SAMPLE_QUESTION, "external_id": "a/1"}])
    importer.import_manifest(conn, "pandas", [{**SAMPLE_QUESTION, "external_id": "a/1"}])
    with pytest.raises(db.AmbiguousExternalId):
        db.get_question_by_external_id(conn, "a/1")


def test_append_submission_event_roundtrip(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    qid = db.all_questions(conn)[0].id
    eid = db.append_submission_event(
        conn,
        session_key="sk-test",
        user="jim",
        question_id=qid,
        verdict="pass",
        hint_index=None,
        hints_shown=0,
        latency_ms=1000,
        answer_text="def solve(): pass",
        judge_comment=None,
        demonstrates_idiom=True,
        judge_json='{"verdict_proposal":"pass"}',
    )
    assert eid >= 1
    row = conn.execute("SELECT * FROM events WHERE id = ?", (eid,)).fetchone()
    assert row["event_type"] == "submission"
    assert row["session_key"] == "sk-test"
    assert row["verdict"] == "pass"


def test_append_question_event(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    qid = db.all_questions(conn)[0].id
    db.append_question_event(conn, session_key="sk-q", user="jim", question_id=qid)
    row = conn.execute("SELECT * FROM events WHERE event_type = 'question'").fetchone()
    assert row["session_key"] == "sk-q"
    assert row["verdict"] is None


def test_append_hint_event(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    qid = db.all_questions(conn)[0].id
    db.append_hint_event(conn, session_key="sk-h", user="jim", question_id=qid, hint_index=1)
    row = conn.execute("SELECT * FROM events WHERE event_type = 'hint'").fetchone()
    assert row["hint_index"] == 1


def test_append_cheat_event(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    qid = db.all_questions(conn)[0].id
    db.append_cheat_event(conn, session_key="sk-c", user="jim", question_id=qid)
    row = conn.execute("SELECT * FROM events WHERE event_type = 'cheat'").fetchone()
    assert row is not None


def test_hint_count_for_session(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    qid = db.all_questions(conn)[0].id
    assert db.hint_count_for_session(conn, "sk-x", qid) == 0
    db.append_hint_event(conn, session_key="sk-x", user="jim", question_id=qid, hint_index=0)
    db.append_hint_event(conn, session_key="sk-x", user="jim", question_id=qid, hint_index=1)
    assert db.hint_count_for_session(conn, "sk-x", qid) == 2


# ---------------------------------------------------------------------------
# Migration + new helper tests
# ---------------------------------------------------------------------------


def _old_schema_conn():
    """In-memory DB with pre-migration schema (no active col, old events CHECK).

    Foreign-key enforcement is turned on to match the real startup/import
    path (``db.connect()`` sets ``PRAGMA foreign_keys=ON``) — migration
    tests that populate rows before calling ``init_db`` need this enabled
    to exercise the rebuild migrations' FK behavior faithfully.
    """
    conn = _sqlite3.connect(":memory:")
    conn.row_factory = _sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
        CREATE TABLE topics (slug TEXT PRIMARY KEY, chapter TEXT NOT NULL,
                             language TEXT NOT NULL DEFAULT 'python');
        CREATE TABLE questions (
          id INTEGER PRIMARY KEY, external_id TEXT UNIQUE,
          topic TEXT NOT NULL, language TEXT NOT NULL,
          modality TEXT NOT NULL, prompt TEXT NOT NULL, stub TEXT,
          entry_point TEXT NOT NULL DEFAULT 'solve',
          canonical_answer TEXT NOT NULL,
          hints_json TEXT NOT NULL DEFAULT '[]',
          test_cases_json TEXT NOT NULL DEFAULT '[]'
        );
        CREATE TABLE events (
          id INTEGER PRIMARY KEY,
          event_type TEXT NOT NULL
            CHECK (event_type IN ('question','hint','cheat','submission')),
          session_key TEXT, user TEXT NOT NULL,
          question_id INTEGER NOT NULL,
          ts TEXT NOT NULL DEFAULT (datetime('now'))
        );
    """)
    return conn


def test_migration_renames_language_to_grader():
    conn = _old_schema_conn()
    db.init_db(conn)
    qcols = {row[1] for row in conn.execute("PRAGMA table_info(questions)")}
    tcols = {row[1] for row in conn.execute("PRAGMA table_info(topics)")}
    assert "grader" in qcols and "language" not in qcols
    assert "grader" in tcols and "language" not in tcols


def test_migration_adds_active_column():
    conn = _old_schema_conn()
    db.init_db(conn)
    cols = {row[1] for row in conn.execute("PRAGMA table_info(questions)")}
    assert "active" in cols
    conn.execute(
        "INSERT INTO questions (topic, grader, modality, prompt, entry_point, canonical_answer)"
        " VALUES ('t', 'python', 'code', 'q', 'solve', 'a')"
    )
    conn.commit()
    row = conn.execute("SELECT active FROM questions WHERE id = 1").fetchone()
    assert row["active"] == 1
    conn.close()


def test_migration_adds_comment_event_type():
    conn = _old_schema_conn()
    db.init_db(conn)
    conn.execute(
        "INSERT INTO questions (topic, grader, modality, prompt, entry_point, canonical_answer)"
        " VALUES ('t', 'python', 'code', 'q', 'solve', 'a')"
    )
    conn.commit()
    conn.execute("INSERT INTO events (event_type, user, question_id) VALUES ('comment', 'u', 1)")
    conn.commit()
    conn.close()


def test_set_question_active_deactivates(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    result = db.set_question_active(conn, 1, False)
    assert result is False
    row = conn.execute("SELECT active FROM questions WHERE id = 1").fetchone()
    assert row["active"] == 0


def test_set_question_active_toggle(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    assert db.set_question_active(conn, 1, None) is False
    assert db.set_question_active(conn, 1, None) is True


def test_set_question_active_returns_none_for_missing(conn):
    assert db.set_question_active(conn, 999, False) is None


def test_append_comment_event(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    event_id = db.append_comment_event(conn, user="jim", question_id=1, comment="bad question")
    assert isinstance(event_id, int)
    row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    assert row["event_type"] == "comment"
    assert row["answer_text"] == "bad question"
    assert row["user"] == "jim"


# ---------------------------------------------------------------------------
# Task 4: override events + scheduler event reader
# ---------------------------------------------------------------------------

from datetime import UTC, datetime


def _import_one(conn):
    from drill.server import importer as _imp
    from tests.conftest import SAMPLE_QUESTION as _SQ

    _imp.import_questions(conn, [_SQ])
    return db.all_questions(conn)[0].id


def test_append_override_event_soon_and_bury(conn):
    qid = _import_one(conn)
    db.append_override_event(conn, session_key=None, user="jim", question_id=qid, kind="soon")
    db.append_override_event(conn, session_key="s1", user="jim", question_id=qid, kind="bury")
    rows = conn.execute("SELECT event_type FROM events WHERE user='jim' ORDER BY id").fetchall()
    assert [r["event_type"] for r in rows] == ["soon", "bury"]


def test_append_override_event_rejects_bad_kind(conn):
    qid = _import_one(conn)
    try:
        db.append_override_event(conn, session_key=None, user="jim", question_id=qid, kind="nope")
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_scheduler_events_includes_all_kinds_in_order(conn):
    qid = _import_one(conn)
    t = "2024-01-01 12:00:00"
    conn.execute(
        "INSERT INTO events (event_type, user, question_id, ts, verdict, latency_ms, answer_text)"
        " VALUES ('submission','jim',?,?, 'pass', 1000, 'x')",
        (qid, t),
    )
    conn.execute(
        "INSERT INTO events (event_type, user, question_id, ts) VALUES ('cheat','jim',?,?)",
        (qid, "2024-01-01 12:01:00"),
    )
    conn.execute(
        "INSERT INTO events (event_type, user, question_id, ts) VALUES ('bury','jim',?,?)",
        (qid, "2024-01-01 12:02:00"),
    )
    conn.execute(
        "INSERT INTO events (event_type, user, question_id, ts) VALUES ('soon','jim',?,?)",
        (qid, "2024-01-01 12:03:00"),
    )
    conn.commit()
    got = db.scheduler_events_for_user(conn, "jim")
    kinds = [e["kind"] for e in got[qid]]
    assert kinds == ["submission", "cheat", "bury", "soon"]
    assert got[qid][0]["ts"] == datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)


def test_prefill_chars_round_trips(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    eid = db.append_submission_event(
        conn,
        session_key="s",
        user="u",
        question_id=1,
        verdict="pass",
        hint_index=None,
        hints_shown=0,
        latency_ms=1000,
        answer_text="abc",
        judge_comment=None,
        demonstrates_idiom=True,
        judge_json=None,
        prefill_chars=2,
    )
    row = conn.execute("SELECT prefill_chars FROM events WHERE id = ?", (eid,)).fetchone()
    assert row["prefill_chars"] == 2

    evs = db.scheduler_events_for_user(conn, "u")[1]
    assert evs[-1]["prefill_chars"] == 2


def test_prefill_chars_defaults_null(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    db.append_submission_event(
        conn,
        session_key="s",
        user="u",
        question_id=1,
        verdict="pass",
        hint_index=None,
        hints_shown=0,
        latency_ms=1000,
        answer_text="abc",
        judge_comment=None,
        demonstrates_idiom=True,
        judge_json=None,
    )
    evs = db.scheduler_events_for_user(conn, "u")[1]
    assert evs[-1]["prefill_chars"] is None


# ---------------------------------------------------------------------------
# Task 2: corpus column + (corpus, external_id) identity
# ---------------------------------------------------------------------------


def test_corpus_defaults_to_python(conn):
    importer.import_questions(conn, [SAMPLE_QUESTION])
    row = conn.execute("SELECT corpus FROM questions WHERE id = 1").fetchone()
    assert row["corpus"] == "python"


def test_same_external_id_coexists_across_corpora(conn):
    a = {**SAMPLE_QUESTION, "corpus": "python"}
    b = {**SAMPLE_QUESTION, "corpus": "pandas"}
    importer.import_questions(conn, [a])
    importer.import_questions(conn, [b])
    rows = conn.execute(
        "SELECT corpus FROM questions WHERE external_id = ? ORDER BY corpus",
        (SAMPLE_QUESTION["external_id"],),
    ).fetchall()
    assert [r["corpus"] for r in rows] == ["pandas", "python"]


def test_migration_backfills_corpus_and_preserves_events():
    """Corpus rebuild must survive real FK enforcement against populated tables.

    Regression test: the `questions` rebuild (DROP TABLE questions /
    CREATE questions_new / INSERT...SELECT / RENAME) drops the parent side
    of `events.question_id REFERENCES questions(id)`. With FK enforcement
    on (as `db.connect()` sets in production) and a live `events` row
    referencing a question, that DROP used to raise
    `sqlite3.IntegrityError: FOREIGN KEY constraint failed`.

    Rows are inserted against the genuine OLD schema (old column name
    `language`, no `active`/`corpus`, old 4-value events CHECK) *before*
    any migration runs, and `init_db` is called exactly once so the whole
    migration cascade — rename, `active` add, events-CHECK rebuild (which
    (re)establishes the FK), then the corpus rebuild — executes in a
    single pass against populated, FK-enforced tables. This is the
    scenario that must not crash.
    """
    conn = _old_schema_conn()  # FK enforcement is ON (see _old_schema_conn)
    conn.execute(
        "INSERT INTO questions (external_id, topic, language, modality, prompt, entry_point, canonical_answer)"
        " VALUES ('x/y', 't', 'python', 'code', 'q', 'solve', 'a')"
    )
    conn.execute("INSERT INTO events (event_type, user, question_id) VALUES ('question','u',1)")
    conn.commit()
    db.init_db(conn)
    qcols = {row[1] for row in conn.execute("PRAGMA table_info(questions)")}
    assert "corpus" in qcols
    assert conn.execute("SELECT corpus FROM questions WHERE id=1").fetchone()["corpus"] == "python"
    ev_row = conn.execute("SELECT COUNT(*) c, MAX(question_id) qid FROM events").fetchone()
    assert ev_row["c"] == 1
    assert ev_row["qid"] == 1


# ---------------------------------------------------------------------------
# Task 3: corpus-scoped manifest object + orphan-deactivation
# ---------------------------------------------------------------------------


def test_scoped_import_deactivates_absent_in_corpus_only(conn):
    py_a = {**SAMPLE_QUESTION, "external_id": "a/1", "corpus": "python"}
    py_b = {**SAMPLE_QUESTION, "external_id": "b/1", "corpus": "python"}
    pd_a = {**SAMPLE_QUESTION, "external_id": "a/1", "corpus": "pandas"}
    importer.import_manifest(conn, "python", [py_a, py_b])
    importer.import_manifest(conn, "pandas", [pd_a])
    # Re-import python with only a/1 present -> b/1 orphaned.
    _, deactivated = importer.import_manifest(conn, "python", [py_a])
    assert deactivated == ["b/1"]
    active = dict(
        conn.execute("SELECT external_id, active FROM questions WHERE corpus='python'").fetchall()
    )
    assert active == {"a/1": 1, "b/1": 0}
    # pandas untouched
    assert (
        conn.execute("SELECT active FROM questions WHERE corpus='pandas'").fetchone()["active"] == 1
    )


def test_scoped_import_preserves_manual_deactivation(conn):
    q = {**SAMPLE_QUESTION, "external_id": "a/1", "corpus": "python"}
    importer.import_manifest(conn, "python", [q])
    qid = conn.execute("SELECT id FROM questions WHERE external_id='a/1'").fetchone()["id"]
    db.set_question_active(conn, qid, False)  # manual deactivate
    importer.import_manifest(conn, "python", [q])  # present -> active untouched
    assert conn.execute("SELECT active FROM questions WHERE id=?", (qid,)).fetchone()["active"] == 0


def test_scoped_import_ignores_null_external_id_rows(conn):
    """NULL external_id rows can't be identity-matched; they must never be
    treated as orphans by import_manifest's deactivation pass.

    Without the `external_id IS NOT NULL` guard on the orphan SELECT, the
    NULL row is picked up as an "orphan" (None not in present), the
    deactivating UPDATE never matches it (NULL = NULL is not true in SQL),
    and sorting/joining the deactivated list explodes on a None among strs.
    """
    real = {**SAMPLE_QUESTION, "external_id": "a/1", "corpus": "python"}
    importer.import_manifest(conn, "python", [real])
    # Seed a NULL-external_id row directly, mirroring the migration tests'
    # style of inserting rows straight into the schema.
    conn.execute(
        "INSERT INTO questions (corpus, external_id, topic, grader, modality,"
        " prompt, entry_point, canonical_answer, active)"
        " VALUES ('python', NULL, 't', 'python', 'code', 'q', 'solve', 'a', 1)"
    )
    conn.commit()

    _, deactivated = importer.import_manifest(conn, "python", [real])

    assert deactivated == []
    assert all(isinstance(x, str) for x in deactivated)
    null_row = conn.execute(
        "SELECT active FROM questions WHERE corpus='python' AND external_id IS NULL"
    ).fetchone()
    assert null_row["active"] == 1


def test_load_manifest_accepts_object_and_list(tmp_path):
    import json

    obj = tmp_path / "m.json"
    obj.write_text(json.dumps({"corpus": "pandas", "questions": [SAMPLE_QUESTION]}))
    corpus, qs = importer.load_manifest(str(obj))
    assert corpus == "pandas" and len(qs) == 1
    arr = tmp_path / "legacy.json"
    arr.write_text(json.dumps([SAMPLE_QUESTION]))
    corpus2, qs2 = importer.load_manifest(str(arr))
    assert corpus2 is None and len(qs2) == 1


def test_load_manifest_rejects_object_missing_corpus(tmp_path):
    """A {"questions": [...]} object without a "corpus" key must raise, not
    silently degrade to the legacy (None, ...) no-deactivation path."""
    import json

    obj = tmp_path / "m.json"
    obj.write_text(json.dumps({"questions": [SAMPLE_QUESTION]}))
    with pytest.raises(ValueError):
        importer.load_manifest(str(obj))
