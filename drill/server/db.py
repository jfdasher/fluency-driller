"""SQLite persistence for the proctor service.

The server is stateless; all state lives in this one database file. ``events``
is strictly append-only — there are no UPDATE or DELETE paths here.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC

from .models import Question, Test
from .srs import SrsConfig

# Stats clamp latency to the same 5-minute cap the grader uses (read-time only;
# raw latency_ms stays untouched in events). Single source: SrsConfig.winsor_ms.
WINSOR_MS = int(SrsConfig().winsor_ms)

SCHEMA = """
CREATE TABLE IF NOT EXISTS topics (
  slug        TEXT NOT NULL,
  corpus      TEXT NOT NULL DEFAULT 'python',
  chapter     TEXT NOT NULL,
  description TEXT,
  tier        INTEGER,
  tier_intv   TEXT,
  signal      TEXT,
  grader      TEXT NOT NULL DEFAULT 'python',
  UNIQUE(corpus, slug)
);

CREATE TABLE IF NOT EXISTS questions (
  id               INTEGER PRIMARY KEY,
  corpus           TEXT NOT NULL DEFAULT 'python',
  external_id      TEXT,
  topic            TEXT NOT NULL,
  grader           TEXT NOT NULL,
  modality         TEXT NOT NULL CHECK (modality IN ('code','fill_in')),
  prompt           TEXT NOT NULL,
  stub             TEXT,
  entry_point      TEXT NOT NULL DEFAULT 'solve',
  canonical_answer TEXT NOT NULL,
  hints_json       TEXT NOT NULL DEFAULT '[]',
  test_cases_json  TEXT NOT NULL DEFAULT '[]',
  active           INTEGER NOT NULL DEFAULT 1,
  UNIQUE(corpus, external_id)
);

CREATE TABLE IF NOT EXISTS events (
  id                 INTEGER PRIMARY KEY,
  event_type         TEXT NOT NULL CHECK (event_type IN ('question','hint','cheat','submission','comment','soon','bury')),
  session_key        TEXT,
  user               TEXT NOT NULL,
  question_id        INTEGER NOT NULL REFERENCES questions(id),
  ts                 TEXT NOT NULL DEFAULT (datetime('now')),
  verdict            TEXT CHECK (verdict IN ('pass','pass_hinted','fail')),
  hints_shown        INTEGER,
  latency_ms         INTEGER,
  answer_text        TEXT,
  judge_comment      TEXT,
  demonstrates_idiom INTEGER,
  judge_json         TEXT,
  hint_index         INTEGER,
  prefill_chars      INTEGER
);
"""


def _migrate_events_event_types(conn: sqlite3.Connection) -> None:
    """Recreate events table with the full 7-value event_type CHECK."""
    # Determine which columns exist in the current events table so we can
    # copy only those columns (handles both old 6-col and current 14-col DBs).
    existing = [row[1] for row in conn.execute("PRAGMA table_info(events)")]
    col_list = ", ".join(existing)
    conn.executescript(f"""
        BEGIN;
        CREATE TABLE events_new (
          id                 INTEGER PRIMARY KEY,
          event_type         TEXT NOT NULL CHECK (event_type IN ('question','hint','cheat','submission','comment','soon','bury')),
          session_key        TEXT,
          user               TEXT NOT NULL,
          question_id        INTEGER NOT NULL REFERENCES questions(id),
          ts                 TEXT NOT NULL DEFAULT (datetime('now')),
          verdict            TEXT CHECK (verdict IN ('pass','pass_hinted','fail')),
          hints_shown        INTEGER,
          latency_ms         INTEGER,
          answer_text        TEXT,
          judge_comment      TEXT,
          demonstrates_idiom INTEGER,
          judge_json         TEXT,
          hint_index         INTEGER
        );
        INSERT INTO events_new ({col_list}) SELECT {col_list} FROM events;
        DROP TABLE events;
        ALTER TABLE events_new RENAME TO events;
        COMMIT;
    """)


class _MedianAgg:
    def __init__(self):
        self._values: list[int] = []

    def step(self, value):
        if value is not None:
            self._values.append(value)

    def finalize(self):
        if not self._values:
            return None
        s = sorted(self._values)
        n = len(s)
        mid = n // 2
        return (s[mid - 1] + s[mid]) // 2 if n % 2 == 0 else s[mid]


def _rename_language_to_grader(conn: sqlite3.Connection, table: str) -> None:
    cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
    if "language" in cols and "grader" not in cols:
        conn.execute(f"ALTER TABLE {table} RENAME COLUMN language TO grader")


def _migrate_questions_add_corpus(conn: sqlite3.Connection) -> None:
    cols = {row[1] for row in conn.execute("PRAGMA table_info(questions)")}
    if "corpus" in cols:
        return
    existing = [row[1] for row in conn.execute("PRAGMA table_info(questions)")]
    copy_cols = ", ".join(existing)
    # Rebuilding the table means DROP TABLE questions, which — with FK
    # enforcement ON and any events row referencing a question — raises
    # sqlite3.IntegrityError. Foreign keys can only be toggled outside an
    # open transaction, so this must wrap the executescript call, not sit
    # inside its own BEGIN/COMMIT.
    conn.execute("PRAGMA foreign_keys=OFF")
    conn.executescript(f"""
        BEGIN;
        CREATE TABLE questions_new (
          id INTEGER PRIMARY KEY,
          corpus TEXT NOT NULL DEFAULT 'python',
          external_id TEXT, topic TEXT NOT NULL, grader TEXT NOT NULL,
          modality TEXT NOT NULL CHECK (modality IN ('code','fill_in')),
          prompt TEXT NOT NULL, stub TEXT,
          entry_point TEXT NOT NULL DEFAULT 'solve',
          canonical_answer TEXT NOT NULL,
          hints_json TEXT NOT NULL DEFAULT '[]',
          test_cases_json TEXT NOT NULL DEFAULT '[]',
          active INTEGER NOT NULL DEFAULT 1,
          UNIQUE(corpus, external_id)
        );
        INSERT INTO questions_new ({copy_cols}) SELECT {copy_cols} FROM questions;
        DROP TABLE questions;
        ALTER TABLE questions_new RENAME TO questions;
        COMMIT;
    """)
    conn.execute("PRAGMA foreign_keys=ON")


def _migrate_topics_add_corpus(conn: sqlite3.Connection) -> None:
    cols = {row[1] for row in conn.execute("PRAGMA table_info(topics)")}
    if "corpus" in cols:
        return
    existing = [row[1] for row in conn.execute("PRAGMA table_info(topics)")]
    copy_cols = ", ".join(existing)
    # No live FK references topics today, but toggle symmetrically with
    # _migrate_questions_add_corpus so both rebuilds behave identically
    # regardless of future FK additions.
    conn.execute("PRAGMA foreign_keys=OFF")
    conn.executescript(f"""
        BEGIN;
        CREATE TABLE topics_new (
          slug TEXT NOT NULL, corpus TEXT NOT NULL DEFAULT 'python',
          chapter TEXT NOT NULL, description TEXT, tier INTEGER,
          tier_intv TEXT, signal TEXT, grader TEXT NOT NULL DEFAULT 'python',
          UNIQUE(corpus, slug)
        );
        INSERT INTO topics_new ({copy_cols}) SELECT {copy_cols} FROM topics;
        DROP TABLE topics;
        ALTER TABLE topics_new RENAME TO topics;
        COMMIT;
    """)
    conn.execute("PRAGMA foreign_keys=ON")


def connect(db_path: str) -> sqlite3.Connection:
    """Open a connection with WAL journaling and row access by column name."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.create_aggregate("median", 1, _MedianAgg)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    existing_cols = {row[1] for row in conn.execute("PRAGMA table_info(topics)")}
    for col, defn in [("tier_intv", "TEXT"), ("signal", "TEXT")]:
        if col not in existing_cols:
            conn.execute(f"ALTER TABLE topics ADD COLUMN {col} {defn}")
    q_cols = {row[1] for row in conn.execute("PRAGMA table_info(questions)")}
    if "active" not in q_cols:
        conn.execute("ALTER TABLE questions ADD COLUMN active INTEGER NOT NULL DEFAULT 1")
    events_sql = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='events'"
    ).fetchone()
    if events_sql and "'soon'" not in events_sql["sql"]:
        _migrate_events_event_types(conn)
    ev_cols = {row[1] for row in conn.execute("PRAGMA table_info(events)")}
    if "prefill_chars" not in ev_cols:
        conn.execute("ALTER TABLE events ADD COLUMN prefill_chars INTEGER")
    for _t in ("questions", "topics"):
        _rename_language_to_grader(conn, _t)
    _migrate_questions_add_corpus(conn)
    _migrate_topics_add_corpus(conn)
    conn.commit()


def _row_to_question(row: sqlite3.Row) -> Question:
    return Question(
        id=row["id"],
        corpus=row["corpus"],
        external_id=row["external_id"],
        topic=row["topic"],
        grader=row["grader"],
        modality=row["modality"],
        prompt=row["prompt"],
        stub=row["stub"],
        entry_point=row["entry_point"],
        canonical_answer=row["canonical_answer"],
        hints=json.loads(row["hints_json"]),
        test_cases=[Test(**tc) for tc in json.loads(row["test_cases_json"])],
    )


def get_question(conn: sqlite3.Connection, question_id: int) -> Question | None:
    row = conn.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
    return _row_to_question(row) if row else None


class AmbiguousExternalId(Exception):
    def __init__(self, external_id: str, corpora: list[str]):
        self.external_id = external_id
        self.corpora = corpora
        super().__init__(f"external_id {external_id!r} exists in corpora: {', '.join(corpora)}")


def get_question_by_external_id(
    conn: sqlite3.Connection, external_id: str, corpus: str | None = None
) -> Question | None:
    if corpus is not None:
        row = conn.execute(
            "SELECT * FROM questions WHERE corpus = ? AND external_id = ?",
            (corpus, external_id),
        ).fetchone()
        return _row_to_question(row) if row else None
    rows = conn.execute("SELECT * FROM questions WHERE external_id = ?", (external_id,)).fetchall()
    if not rows:
        return None
    if len(rows) > 1:
        raise AmbiguousExternalId(external_id, sorted(r["corpus"] for r in rows))
    return _row_to_question(rows[0])


def all_questions(conn: sqlite3.Connection) -> list[Question]:
    rows = conn.execute("SELECT * FROM questions ORDER BY id").fetchall()
    return [_row_to_question(r) for r in rows]


def append_submission_event(
    conn: sqlite3.Connection,
    *,
    session_key: str | None,
    user: str,
    question_id: int,
    verdict: str,
    hint_index: int | None,
    hints_shown: int,
    latency_ms: int | None,
    answer_text: str,
    judge_comment: str | None,
    demonstrates_idiom: bool | None,
    judge_json: str | None,
    prefill_chars: int | None = None,
) -> int:
    """Append a submission event and return its id."""
    cur = conn.execute(
        """
        INSERT INTO events (
            event_type, session_key, user, question_id, verdict, hint_index,
            hints_shown, latency_ms, answer_text, judge_comment,
            demonstrates_idiom, judge_json, prefill_chars
        ) VALUES ('submission', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_key,
            user,
            question_id,
            verdict,
            hint_index,
            hints_shown,
            latency_ms,
            answer_text,
            judge_comment,
            None if demonstrates_idiom is None else int(demonstrates_idiom),
            judge_json,
            prefill_chars,
        ),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def append_question_event(
    conn: sqlite3.Connection,
    *,
    session_key: str,
    user: str,
    question_id: int,
) -> int:
    cur = conn.execute(
        "INSERT INTO events (event_type, session_key, user, question_id)"
        " VALUES ('question', ?, ?, ?)",
        (session_key, user, question_id),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def append_hint_event(
    conn: sqlite3.Connection,
    *,
    session_key: str,
    user: str,
    question_id: int,
    hint_index: int,
) -> int:
    cur = conn.execute(
        "INSERT INTO events (event_type, session_key, user, question_id, hint_index)"
        " VALUES ('hint', ?, ?, ?, ?)",
        (session_key, user, question_id, hint_index),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def append_cheat_event(
    conn: sqlite3.Connection,
    *,
    session_key: str,
    user: str,
    question_id: int,
) -> int:
    cur = conn.execute(
        "INSERT INTO events (event_type, session_key, user, question_id) VALUES ('cheat', ?, ?, ?)",
        (session_key, user, question_id),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def append_override_event(
    conn: sqlite3.Connection,
    *,
    session_key: str | None,
    user: str,
    question_id: int,
    kind: str,
) -> int:
    """Append a 'soon' or 'bury' scheduler-override event; return its id."""
    if kind not in ("soon", "bury"):
        raise ValueError(f"invalid override kind: {kind!r}")
    cur = conn.execute(
        "INSERT INTO events (event_type, session_key, user, question_id) VALUES (?, ?, ?, ?)",
        (kind, session_key, user, question_id),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def set_question_active(
    conn: sqlite3.Connection,
    question_id: int,
    active: bool | None,
) -> bool | None:
    """Set or toggle active status. Returns new value, or None if not found."""
    row = conn.execute("SELECT active FROM questions WHERE id = ?", (question_id,)).fetchone()
    if row is None:
        return None
    new_active = (not bool(row["active"])) if active is None else active
    conn.execute(
        "UPDATE questions SET active = ? WHERE id = ?",
        (int(new_active), question_id),
    )
    conn.commit()
    return new_active


def append_comment_event(
    conn: sqlite3.Connection,
    *,
    user: str,
    question_id: int,
    comment: str,
) -> int:
    """Append a user comment event and return its id."""
    cur = conn.execute(
        "INSERT INTO events (event_type, user, question_id, answer_text)"
        " VALUES ('comment', ?, ?, ?)",
        (user, question_id, comment),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def submission_events_for_user(conn: sqlite3.Connection, user: str) -> dict[int, list[dict]]:
    """Return submission events for a user, grouped by question_id.

    Each event dict has: ts (datetime, UTC), verdict, hints_shown,
    latency_ms, answer_text. Within each group events are ordered ts, id.
    """
    from datetime import datetime

    rows = conn.execute(
        """
        SELECT question_id, ts, verdict, hints_shown, latency_ms, answer_text
        FROM events
        WHERE user = ? AND event_type = 'submission'
        ORDER BY question_id, ts, id
        """,
        (user,),
    ).fetchall()

    result: dict[int, list[dict]] = {}
    for row in rows:
        qid = row["question_id"]
        ts_str = row["ts"]
        ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
        result.setdefault(qid, []).append(
            {
                "ts": ts,
                "verdict": row["verdict"],
                "hints_shown": row["hints_shown"] or 0,
                "latency_ms": row["latency_ms"],
                "answer_text": row["answer_text"] or "",
            }
        )
    return result


def scheduler_events_for_user(conn: sqlite3.Connection, user: str) -> dict[int, list[dict]]:
    """Return scheduler-relevant events grouped by question_id, ts/id-ordered.

    Includes submission, cheat, soon, and bury events. Each dict carries:
    kind, ts (UTC datetime), verdict, hints_shown, latency_ms, answer_text.
    """
    from datetime import datetime

    rows = conn.execute(
        """
        SELECT question_id, ts, event_type, verdict, hints_shown, latency_ms,
               answer_text, prefill_chars
        FROM events
        WHERE user = ? AND event_type IN ('submission','cheat','soon','bury')
        ORDER BY question_id, ts, id
        """,
        (user,),
    ).fetchall()

    result: dict[int, list[dict]] = {}
    for row in rows:
        qid = row["question_id"]
        ts = datetime.strptime(row["ts"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
        result.setdefault(qid, []).append(
            {
                "kind": row["event_type"],
                "ts": ts,
                "verdict": row["verdict"],
                "hints_shown": row["hints_shown"] or 0,
                "latency_ms": row["latency_ms"],
                "answer_text": row["answer_text"] or "",
                "prefill_chars": row["prefill_chars"],
            }
        )
    return result


def _date_filter(
    date_range: str | None,
    date_range_start: str | None,
    date_range_end: str | None,
) -> tuple[str, list]:
    """Return (sql_fragment, params) for an optional date range WHERE clause."""
    if date_range == "today":
        return "AND DATE(ts) = DATE('now')", []
    if date_range == "7days":
        return "AND ts >= DATE('now', '-7 days')", []
    if date_range == "30days":
        return "AND ts >= DATE('now', '-30 days')", []
    if date_range_start and date_range_end:
        return "AND DATE(ts) BETWEEN ? AND ?", [date_range_start, date_range_end]
    if date_range_start:
        return "AND DATE(ts) >= ?", [date_range_start]
    return "", []


def stats_session(conn: sqlite3.Connection, session_key: str, user: str) -> dict:
    """Aggregate all events for one study session."""
    row = conn.execute(
        f"""
        SELECT
            SUM(CASE WHEN event_type = 'submission' THEN 1 ELSE 0 END)       AS questions,
            SUM(CASE WHEN verdict = 'pass'          THEN 1 ELSE 0 END)       AS pass_count,
            SUM(CASE WHEN verdict = 'pass_hinted'   THEN 1 ELSE 0 END)       AS pass_hinted,
            SUM(CASE WHEN verdict = 'fail'          THEN 1 ELSE 0 END)       AS fail,
            SUM(CASE WHEN event_type = 'hint'       THEN 1 ELSE 0 END)       AS hints_used,
            SUM(CASE WHEN event_type = 'cheat'      THEN 1 ELSE 0 END)       AS cheats,
            CAST(AVG(CASE WHEN event_type = 'submission' THEN MIN(latency_ms, {WINSOR_MS}) END)
                 AS INTEGER)                                                   AS avg_latency_ms,
            CAST(median(CASE WHEN event_type = 'submission' THEN MIN(latency_ms, {WINSOR_MS}) END)
                 AS INTEGER)                                                   AS median_latency_ms
        FROM events
        WHERE session_key = ? AND user = ?
        """,
        (session_key, user),
    ).fetchone()
    if row is None or row["questions"] is None:
        return {
            "questions": 0,
            "pass_count": 0,
            "pass_hinted": 0,
            "fail": 0,
            "hints_used": 0,
            "cheats": 0,
            "avg_latency_ms": None,
            "median_latency_ms": None,
        }
    return dict(row)


def stats_day(conn: sqlite3.Connection, user: str) -> dict:
    """Aggregate all events for the current local calendar day."""
    row = conn.execute(
        f"""
        SELECT
            DATE('now', 'localtime')                                                   AS date,
            COALESCE(SUM(CASE WHEN event_type = 'submission' THEN 1 ELSE 0 END), 0)   AS questions,
            COALESCE(SUM(CASE WHEN verdict = 'pass'          THEN 1 ELSE 0 END), 0)   AS pass_count,
            COALESCE(SUM(CASE WHEN verdict = 'pass_hinted'   THEN 1 ELSE 0 END), 0)   AS pass_hinted,
            COALESCE(SUM(CASE WHEN verdict = 'fail'          THEN 1 ELSE 0 END), 0)   AS fail,
            COALESCE(SUM(CASE WHEN event_type = 'hint'       THEN 1 ELSE 0 END), 0)   AS hints_used,
            COALESCE(SUM(CASE WHEN event_type = 'cheat'      THEN 1 ELSE 0 END), 0)   AS cheats,
            CAST(AVG(CASE WHEN event_type = 'submission' THEN MIN(latency_ms, {WINSOR_MS}) END)
                 AS INTEGER)                                                            AS avg_latency_ms,
            CAST(median(CASE WHEN event_type = 'submission' THEN MIN(latency_ms, {WINSOR_MS}) END)
                 AS INTEGER)                                                            AS median_latency_ms
        FROM events
        WHERE user = ?
          AND DATE(ts, 'localtime') = DATE('now', 'localtime')
        """,
        (user,),
    ).fetchone()
    return dict(row)


def stats_topics(
    conn: sqlite3.Connection,
    user: str,
    grader: str | None = None,
    date_range: str | None = None,
    date_range_start: str | None = None,
    date_range_end: str | None = None,
    corpus: str | None = None,
) -> list[dict]:
    date_sql, date_params = _date_filter(date_range, date_range_start, date_range_end)
    lang_sql = "AND q.grader = ?" if grader else ""
    lang_params = [grader] if grader else []
    corpus_sql = "AND q.corpus = ?" if corpus else ""
    corpus_params = [corpus] if corpus else []
    rows = conn.execute(
        f"""
        SELECT
            q.topic,
            COUNT(*)                                                                  AS attempts,
            SUM(CASE WHEN e.verdict = 'pass'        THEN 1 ELSE 0 END)              AS pass_count,
            SUM(CASE WHEN e.verdict = 'pass_hinted' THEN 1 ELSE 0 END)              AS pass_hinted,
            SUM(CASE WHEN e.verdict = 'fail'        THEN 1 ELSE 0 END)              AS fail,
            ROUND(SUM(CASE WHEN e.verdict IN ('pass','pass_hinted') THEN 1.0 ELSE 0 END)
                  / COUNT(*), 3)                                                      AS pass_rate,
            ROUND(SUM(CASE WHEN e.verdict = 'pass'  THEN 1.0 ELSE 0 END)
                  / COUNT(*), 3)                                                      AS clean_pass_rate,
            CAST(AVG(MIN(e.latency_ms, {WINSOR_MS})) AS INTEGER)                     AS avg_latency_ms
        FROM events e
        JOIN questions q ON q.id = e.question_id
        WHERE e.user = ? AND e.event_type = 'submission'
          {lang_sql} {corpus_sql} {date_sql}
        GROUP BY q.topic
        ORDER BY pass_rate ASC, q.topic ASC
        """,
        (user, *lang_params, *corpus_params, *date_params),
    ).fetchall()
    return [dict(r) for r in rows]


def stats_trends(
    conn: sqlite3.Connection,
    user: str,
    date_range: str | None = "30days",
    date_range_start: str | None = None,
    date_range_end: str | None = None,
) -> list[dict]:
    date_sql, date_params = _date_filter(date_range, date_range_start, date_range_end)
    rows = conn.execute(
        f"""
        SELECT
            DATE(ts)                                                                   AS date,
            COUNT(*)                                                                   AS attempts,
            SUM(CASE WHEN verdict = 'pass'        THEN 1 ELSE 0 END)                 AS pass_count,
            SUM(CASE WHEN verdict = 'pass_hinted' THEN 1 ELSE 0 END)                 AS pass_hinted,
            SUM(CASE WHEN verdict = 'fail'        THEN 1 ELSE 0 END)                 AS fail,
            ROUND(SUM(CASE WHEN verdict IN ('pass','pass_hinted') THEN 1.0 ELSE 0 END)
                  / COUNT(*), 3)                                                       AS pass_rate,
            CAST(AVG(MIN(latency_ms, {WINSOR_MS})) AS INTEGER)                        AS avg_latency_ms
        FROM events
        WHERE user = ? AND event_type = 'submission'
          {date_sql}
        GROUP BY DATE(ts)
        ORDER BY date ASC
        """,
        (user, *date_params),
    ).fetchall()
    return [dict(r) for r in rows]


def stats_cards(
    conn: sqlite3.Connection,
    user: str,
    topic: str | None = None,
    date_range: str | None = None,
    date_range_start: str | None = None,
    date_range_end: str | None = None,
    corpus: str | None = None,
) -> list[dict]:
    date_sql, date_params = _date_filter(date_range, date_range_start, date_range_end)
    topic_pattern = f"%{topic}%" if topic else "%"
    corpus_sql = "AND q.corpus = ?" if corpus else ""
    corpus_params = [corpus] if corpus else []
    rows = conn.execute(
        f"""
        SELECT
            q.id                                                                        AS question_id,
            q.external_id,
            q.topic,
            SUM(CASE WHEN e.event_type = 'submission' THEN 1 ELSE 0 END)              AS attempts,
            SUM(CASE WHEN e.verdict IN ('pass','pass_hinted') THEN 1 ELSE 0 END)      AS pass_count,
            (SELECT verdict FROM events sub
             WHERE sub.question_id = q.id AND sub.user = ?
               AND sub.event_type = 'submission'
             ORDER BY sub.ts DESC, sub.id DESC LIMIT 1)                                 AS last_verdict,
            CAST(AVG(CASE WHEN e.event_type = 'submission' THEN MIN(e.latency_ms, {WINSOR_MS}) END)
                 AS INTEGER)                                                             AS avg_latency_ms,
            SUM(CASE WHEN e.event_type = 'hint'  THEN 1 ELSE 0 END)                   AS hints_ever,
            CASE WHEN SUM(CASE WHEN e.event_type = 'cheat' THEN 1 ELSE 0 END) > 0
                 THEN 1 ELSE 0 END                                                      AS cheated
        FROM questions q
        JOIN events e ON e.question_id = q.id
        WHERE e.user = ?
          AND q.topic LIKE ?
          {corpus_sql} {date_sql}
        GROUP BY q.id
        ORDER BY q.topic ASC, q.id ASC
        """,
        (user, user, topic_pattern, *corpus_params, *date_params),
    ).fetchall()
    return [dict(r) for r in rows]


def stats_coverage(
    conn: sqlite3.Connection,
    user: str,
    grader: str | None = None,
    corpus: str | None = None,
) -> list[dict]:
    lang_sql = "AND q.grader = ?" if grader else ""
    lang_params = [grader] if grader else []
    corpus_sql = "AND q.corpus = ?" if corpus else ""
    corpus_params = [corpus] if corpus else []
    rows = conn.execute(
        f"""
        SELECT
            q.topic,
            COUNT(DISTINCT q.id)                                                       AS total_questions,
            COUNT(DISTINCT e.question_id)                                              AS attempted,
            ROUND(COUNT(DISTINCT e.question_id) * 1.0 / COUNT(DISTINCT q.id), 3)     AS coverage_pct,
            ROUND(
                SUM(CASE WHEN e.verdict IN ('pass','pass_hinted') THEN 1.0 ELSE 0 END)
                / NULLIF(COUNT(CASE WHEN e.event_type = 'submission' THEN 1 END), 0),
                3)                                                                      AS pass_rate
        FROM questions q
        LEFT JOIN events e ON e.question_id = q.id
            AND e.user = ?
            AND e.event_type = 'submission'
        WHERE 1=1 {lang_sql} {corpus_sql}
        GROUP BY q.topic
        ORDER BY coverage_pct ASC, q.topic ASC
        """,
        (user, *lang_params, *corpus_params),
    ).fetchall()
    return [dict(r) for r in rows]


def hint_count_for_session(conn: sqlite3.Connection, session_key: str, question_id: int) -> int:
    row = conn.execute(
        "SELECT COUNT(*) AS c FROM events"
        " WHERE session_key = ? AND question_id = ? AND event_type = 'hint'",
        (session_key, question_id),
    ).fetchone()
    return row["c"] if row else 0
