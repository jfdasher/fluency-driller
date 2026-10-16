"""Seed-content quality gates (PRD §11) and self-consistency."""

import json
import pathlib

from drill._runner import run_tests
from drill.server import db, importer

SEED = pathlib.Path(__file__).resolve().parents[1] / "drill" / "data" / "seed_questions.json"


def _load():
    return json.loads(SEED.read_text())


def test_seed_meets_prd_minimums():
    qs = _load()
    assert len(qs) >= 15
    assert len({q["topic"] for q in qs}) >= 4
    for q in qs:
        assert len(q["hints"]) == 3, q["external_id"]
        assert len(q["test_cases"]) >= 2, q["external_id"]


def test_all_questions_have_three_hints():
    for q in _load():
        assert len(q["hints"]) == 3, f"{q['external_id']} has {len(q['hints'])} hints, expected 3"


def test_first_question_is_the_multi_key_stable_sort():
    assert "multi-key-stable" in _load()[0]["external_id"]


def test_external_ids_are_unique():
    ids = [q["external_id"] for q in _load()]
    assert len(ids) == len(set(ids))


def test_every_canonical_answer_passes_its_own_cases():
    for q in _load():
        ns: dict = {}
        exec(q["canonical_answer"], ns)
        out = run_tests(ns, q.get("entry_point", "solve"), q["test_cases"])
        assert out["failed"] == 0, f"{q['external_id']}: {out['detail']}"


def test_seed_imports_cleanly(conn):
    n = importer.import_questions(conn, _load())
    assert n == len(_load())
    assert len(db.all_questions(conn)) == len(_load())
