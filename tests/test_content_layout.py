from drill.content.layout import dump_question_dir, load_question_dir, validate_question_dir
from drill.content.schema import ContentQuestion, Test


def _q():
    return ContentQuestion(
        external_id="functions/closures/factory",
        topic="functions/closures",
        kind="idiom",
        status="approved",
        prompt="Write `make(f)` returning a closure.",
        stub="def make(f):\n    ...",
        entry_point="make",
        canonical_answer="def make(f):\n    return lambda x: x * f",
        hints=["Return an inner function.", "It captures `f`.", "`def inner(x): return x*f`."],
        tests=[Test(name="test_basic", source="def test_basic():\n    assert make(3)(5) == 15")],
        provenance={"model": "m", "verified": {"ok": True}},
    )


def test_dump_then_load_round_trips(tmp_path):
    d = tmp_path / "factory"
    dump_question_dir(_q(), d)
    assert (d / "question.md").exists()
    assert (d / "stub.py").read_text().startswith("def make")
    assert (d / "canonical_answer.py").read_text().startswith("def make")
    assert (d / "tests" / "test_basic.py").exists()
    loaded = load_question_dir(d)
    assert loaded.entry_point == "make"
    assert loaded.prompt == "Write `make(f)` returning a closure."
    assert loaded.hints == [
        "Return an inner function.",
        "It captures `f`.",
        "`def inner(x): return x*f`.",
    ]
    assert loaded.tests[0].name == "test_basic"
    assert "assert make(3)(5) == 15" in loaded.tests[0].source


def test_validate_flags_wrong_hint_count(tmp_path):
    q = _q()
    q.hints = ["only", "two"]
    d = tmp_path / "bad"
    dump_question_dir(q, d)
    problems = validate_question_dir(d)
    assert any("hint" in p.lower() for p in problems)


def test_validate_ok_returns_empty(tmp_path):
    d = tmp_path / "good"
    dump_question_dir(_q(), d)
    assert validate_question_dir(d) == []
