"""Idempotent question import.

Reads a JSON array of question objects and upserts them on ``external_id`` so
prompts stay editable without creating duplicates. Run as:

    python -m drill.server.importer questions.json

(or via the ``drill-import`` console script). Uses ``DRILL_DB_PATH``.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from typing import Any

from . import db


def _normalize(q: dict[str, Any]) -> dict[str, Any]:
    if not q.get("external_id"):
        raise ValueError(f"question missing required 'external_id': {q.get('topic', q)!r}")
    return {
        "corpus": q.get("corpus", "python"),
        "external_id": q["external_id"],
        "topic": q["topic"],
        "grader": q["grader"],
        "modality": q.get("modality", "code"),
        "prompt": q["prompt"],
        "stub": q.get("stub"),
        "entry_point": q.get("entry_point", "solve"),
        "canonical_answer": q["canonical_answer"],
        "hints_json": json.dumps(q.get("hints", [])),
        "test_cases_json": json.dumps(q.get("test_cases", [])),
    }


def import_questions(conn: sqlite3.Connection, questions: list[dict[str, Any]]) -> int:
    """Upsert questions on ``external_id``. Returns the number processed."""
    rows = [_normalize(q) for q in questions]
    conn.executemany(
        """
        INSERT INTO questions (
            corpus, external_id, topic, grader, modality, prompt, stub,
            entry_point, canonical_answer, hints_json, test_cases_json
        ) VALUES (
            :corpus, :external_id, :topic, :grader, :modality, :prompt, :stub,
            :entry_point, :canonical_answer, :hints_json, :test_cases_json
        )
        ON CONFLICT(corpus, external_id) DO UPDATE SET
            topic            = excluded.topic,
            grader           = excluded.grader,
            modality         = excluded.modality,
            prompt           = excluded.prompt,
            stub             = excluded.stub,
            entry_point      = excluded.entry_point,
            canonical_answer = excluded.canonical_answer,
            hints_json       = excluded.hints_json,
            test_cases_json  = excluded.test_cases_json
        """,
        rows,
    )
    conn.commit()
    return len(rows)


def import_manifest(
    conn: sqlite3.Connection, corpus: str, questions: list[dict[str, Any]]
) -> tuple[int, list[str]]:
    """Upsert `questions` into `corpus`, then deactivate that corpus's orphans.

    Orphan = an active question in `corpus` whose external_id is absent from
    `questions`. Present rows keep their `active` flag (sticky-manual). Returns
    (processed, deactivated_external_ids).
    """
    stamped = [{**q, "corpus": corpus} for q in questions]
    n = import_questions(conn, stamped)
    present = {q["external_id"] for q in stamped}
    rows = conn.execute(
        "SELECT external_id FROM questions"
        " WHERE corpus = ? AND active = 1 AND external_id IS NOT NULL",
        (corpus,),
    ).fetchall()
    orphans = sorted(r["external_id"] for r in rows if r["external_id"] not in present)
    for ext in orphans:
        conn.execute(
            "UPDATE questions SET active = 0 WHERE corpus = ? AND external_id = ?",
            (corpus, ext),
        )
    conn.commit()
    return n, orphans


def load_manifest(path: str) -> tuple[str | None, list[dict[str, Any]]]:
    """Return (corpus, questions). corpus is None for a legacy bare-array file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return None, data
    if isinstance(data, dict) and "questions" in data:
        if "corpus" not in data:
            raise ValueError("manifest object must carry a 'corpus' key alongside 'questions'")
        return data["corpus"], data["questions"]
    raise ValueError("manifest must be a JSON array or a {corpus, questions} object")


def import_topics(conn: sqlite3.Connection, topics: list[dict[str, Any]]) -> int:
    """Upsert topics on ``slug``. Returns the number processed."""
    rows = []
    for t in topics:
        if not t.get("slug"):
            raise ValueError(f"topic missing required 'slug': {t!r}")
        rows.append(
            {
                "slug": t["slug"],
                "corpus": t.get("corpus", "python"),
                "chapter": t["chapter"],
                "description": t.get("description"),
                "tier": t.get("tier"),
                "tier_intv": t.get("tier_intv"),
                "signal": t.get("signal"),
                "grader": t.get("grader", "python"),
            }
        )
    conn.executemany(
        """
        INSERT INTO topics (slug, corpus, chapter, description, tier, tier_intv, signal, grader)
        VALUES (:slug, :corpus, :chapter, :description, :tier, :tier_intv, :signal, :grader)
        ON CONFLICT(corpus, slug) DO UPDATE SET
            chapter     = excluded.chapter,
            description = excluded.description,
            tier        = excluded.tier,
            tier_intv   = excluded.tier_intv,
            signal      = excluded.signal,
            grader      = excluded.grader
        """,
        rows,
    )
    conn.commit()
    return len(rows)


def load_topics(path: str) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("topics file must be a JSON array")
    return data


def import_topics_main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: drill-import-topics <topics.json>", file=sys.stderr)
        return 2
    db_path = os.environ.get("DRILL_DB_PATH", "drill.db")
    conn = db.connect(db_path)
    db.init_db(conn)
    n = import_topics(conn, load_topics(argv[0]))
    conn.close()
    print(f"imported {n} topic(s) into {db_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: python -m drill.server.importer <questions.json>", file=sys.stderr)
        return 2
    db_path = os.environ.get("DRILL_DB_PATH", "drill.db")
    conn = db.connect(db_path)
    db.init_db(conn)
    corpus, questions = load_manifest(argv[0])
    if corpus is None:
        n = import_questions(conn, questions)
        print(f"imported {n} question(s) into {db_path} (legacy, no deactivation)")
    else:
        n, deactivated = import_manifest(conn, corpus, questions)
        print(f"imported {n} question(s) into corpus {corpus!r} in {db_path}")
        if deactivated:
            print(f"deactivated {len(deactivated)} orphan(s): {', '.join(deactivated)}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
