"""Topics table and taxonomy tests."""

import os

import pytest

from drill.server import importer


def test_topics_table_exists(conn):
    """init_db creates the topics table."""
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='topics'"
    ).fetchone()
    assert row is not None, "topics table was not created by init_db"


def test_import_topics_basic(conn):
    """import_topics inserts rows; round-trip via SELECT."""
    topics = [
        {
            "slug": "types/dict",
            "chapter": "types",
            "description": "get/setdefault",
            "tier": 1,
            "grader": "python",
        },
        {
            "slug": "iteration/sorting",
            "chapter": "iteration",
            "description": "key functions",
            "tier": 1,
            "grader": "python",
        },
    ]
    n = importer.import_topics(conn, topics)
    assert n == 2
    rows = conn.execute("SELECT slug FROM topics ORDER BY slug").fetchall()
    assert [r["slug"] for r in rows] == ["iteration/sorting", "types/dict"]


def test_import_topics_upsert(conn):
    """Re-importing same slug updates fields without creating a duplicate."""
    importer.import_topics(
        conn,
        [
            {
                "slug": "types/dict",
                "chapter": "types",
                "description": "old",
                "tier": 2,
                "grader": "python",
            },
        ],
    )
    importer.import_topics(
        conn,
        [
            {
                "slug": "types/dict",
                "chapter": "types",
                "description": "new",
                "tier": 1,
                "grader": "python",
            },
        ],
    )
    rows = conn.execute("SELECT * FROM topics WHERE slug = 'types/dict'").fetchall()
    assert len(rows) == 1
    assert rows[0]["description"] == "new"
    assert rows[0]["tier"] == 1


def test_import_topics_missing_slug_raises(conn):
    """import_topics raises ValueError when slug is missing."""
    with pytest.raises(ValueError, match="slug"):
        importer.import_topics(conn, [{"chapter": "types", "description": "oops"}])


def test_load_topics_from_json_file(conn):
    """topics_python.json loads and imports without error; count == 87."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "drill", "data", "topics_python.json")
    topics = importer.load_topics(data_path)
    assert len(topics) == 87
    n = importer.import_topics(conn, topics)
    assert n == 87
    rows = conn.execute("SELECT COUNT(*) AS c FROM topics").fetchone()
    assert rows["c"] == 87
    corpus_row = conn.execute(
        "SELECT tier_intv, signal FROM topics WHERE slug = 'operators/bitwise'"
    ).fetchone()
    assert corpus_row["signal"] == "corpus"
    assert corpus_row["tier_intv"] == "2"
