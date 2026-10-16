"""Validation for the pandas corpus taxonomy (drill/data/topics_pandas.json)."""

import json
import os

from drill.server import importer

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "drill", "data", "topics_pandas.json")

EXPECTED_CHAPTERS = [
    "numpy-foundations",
    "construction-inspection",
    "dtypes-missing",
    "index",
    "selection",
    "transform-compute",
    "combining",
    "groupby-aggregate-window",
    "reshaping",
    "binning",
    "test-data-synthesis",
    "io-lite",
]


def _load():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def test_is_json_array_of_72():
    topics = _load()
    assert isinstance(topics, list)
    assert len(topics) == 72


def test_every_row_is_pandas_corpus_python_grader():
    for t in _load():
        assert t["corpus"] == "pandas", t
        assert t["grader"] == "python", t


def test_slugs_unique_and_prefixed_by_chapter():
    topics = _load()
    slugs = [t["slug"] for t in topics]
    assert len(slugs) == len(set(slugs)), "duplicate slug"
    for t in topics:
        assert t["slug"].startswith(t["chapter"] + "/"), t
        assert t["slug"].count("/") == 1, t


def test_chapters_match_spec_set():
    chapters = {t["chapter"] for t in _load()}
    assert chapters == set(EXPECTED_CHAPTERS)


def test_tiers_in_range_and_description_present():
    for t in _load():
        assert t["tier"] in (1, 2, 3, 4), t
        assert isinstance(t["description"], str) and t["description"], t


def test_imports_via_import_topics(conn):
    topics = importer.load_topics(DATA_PATH)
    n = importer.import_topics(conn, topics)
    assert n == 72
    row = conn.execute("SELECT COUNT(*) AS c FROM topics WHERE corpus = 'pandas'").fetchone()
    assert row["c"] == 72
