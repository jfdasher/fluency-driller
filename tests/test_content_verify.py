from drill.content.schema import ContentQuestion, Test
from drill.content.verify import verify_question


def _q(canonical, sources, entry_point="make"):
    return ContentQuestion(
        external_id="t/x",
        topic="t",
        kind="idiom",
        prompt="p",
        canonical_answer=canonical,
        entry_point=entry_point,
        tests=[Test(name=f"test_{i}", source=s) for i, s in enumerate(sources)],
    )


def test_passing_canonical_verifies_ok():
    q = _q(
        "def make(f):\n    return lambda x: x * f",
        ["def test_a():\n    assert make(3)(5) == 15", "def test_b():\n    assert fn(0)(9) == 0"],
    )
    r = verify_question(q)
    assert r.ok and r.failures == []


def test_failing_assert_is_reported():
    q = _q(
        "def make(f):\n    return lambda x: x * f", ["def test_a():\n    assert make(3)(5) == 999"]
    )
    r = verify_question(q)
    assert not r.ok
    assert "test_a" in r.failures[0] and "AssertionError" in r.failures[0]


def test_broken_submission_is_reported():
    q = _q(
        "def make(f):\n    return 1/0  # not even callable build",
        ["def test_a():\n    assert make(3) == 1"],
    )
    r = verify_question(q)
    # canonical execs fine; calling make raises ZeroDivisionError inside the test
    assert not r.ok
