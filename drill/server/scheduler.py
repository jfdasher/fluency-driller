"""SM-2 spaced-repetition scheduler.

Replays each candidate card's submission history to compute due_at, then
picks the most overdue card; falls back to the lowest-id NEW card; returns
None when everything is scheduled in the future and no new cards remain.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime

from .db import _row_to_question, scheduler_events_for_user
from .models import Question
from .srs import CardState, SrsConfig, replay


@dataclass(frozen=True)
class Selection:
    """The card to serve next plus a snapshot of what is available right now.

    ``due_count`` and ``new_count`` count every candidate that is due or NEW at
    selection time, *including* the picked card. Their sum is the number of
    questions the scheduler would serve before reporting nothing left.
    """

    question: Question | None
    due_count: int
    new_count: int


_CANDIDATES_SQL = """
SELECT q.*
FROM questions q
WHERE (:grader IS NULL OR q.grader = :grader)
  AND (:topic IS NULL OR q.topic = :topic)
  AND (:topic_keyword IS NULL OR q.topic LIKE '%' || :topic_keyword || '%')
  AND (:corpus IS NULL OR q.corpus = :corpus)
  AND q.active = 1
ORDER BY q.id ASC
"""


def next_question(
    conn: sqlite3.Connection,
    user: str,
    grader: str | None = None,
    topic: str | None = None,
    topic_keyword: str | None = None,
    corpus: str | None = None,
    *,
    now: datetime | None = None,
    cfg: SrsConfig | None = None,
) -> Question | None:
    return select_next(
        conn,
        user,
        grader,
        topic=topic,
        topic_keyword=topic_keyword,
        corpus=corpus,
        now=now,
        cfg=cfg,
    ).question


def select_next(
    conn: sqlite3.Connection,
    user: str,
    grader: str | None = None,
    topic: str | None = None,
    topic_keyword: str | None = None,
    corpus: str | None = None,
    *,
    now: datetime | None = None,
    cfg: SrsConfig | None = None,
) -> Selection:
    if now is None:
        now = datetime.now(UTC)
    if cfg is None:
        cfg = SrsConfig()

    rows = conn.execute(
        _CANDIDATES_SQL,
        {
            "grader": grader,
            "topic": topic,
            "topic_keyword": topic_keyword,
            "corpus": corpus,
        },
    ).fetchall()

    if not rows:
        return Selection(None, 0, 0)

    events_by_qid = scheduler_events_for_user(conn, user)

    due: list[tuple[datetime, int, object]] = []  # (due_at, question_id, row)
    new: list[tuple[int, object]] = []  # (question_id, row) for NEW cards

    for row in rows:
        qid = row["id"]
        events = events_by_qid.get(qid, [])
        state: CardState = replay(events, cfg, now)

        if state.phase == "NEW":
            new.append((qid, row))
        elif state.due_at <= now:
            due.append((state.due_at, qid, row))

    counts = (len(due), len(new))

    if due:
        # Most overdue first (smallest due_at), tiebreak by ascending question_id
        due.sort(key=lambda t: (t[0], t[1]))
        return Selection(_row_to_question(due[0][2]), *counts)

    if new:
        # Lowest-id new card
        new.sort(key=lambda t: t[0])
        return Selection(_row_to_question(new[0][1]), *counts)

    return Selection(None, *counts)
