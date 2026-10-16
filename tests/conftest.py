import pytest

from drill.server import db


@pytest.fixture
def conn():
    """A connected, schema-initialized in-memory SQLite database."""
    c = db.connect(":memory:")
    db.init_db(c)
    yield c
    c.close()


SAMPLE_QUESTION = {
    "external_id": "sorting/multi-key-stable-mixed",
    "topic": "sorting/multi-key-stable",
    "grader": "python",
    "modality": "code",
    "prompt": "Sort dict ascending by int value, descending by key as tiebreak.",
    "stub": "def solve(d):\n    ...",
    "entry_point": "solve",
    "canonical_answer": (
        "def solve(d):\n"
        "    items = sorted(d.items(), key=lambda kv: kv[0], reverse=True)\n"
        "    return [list(kv) for kv in sorted(items, key=lambda kv: int(kv[1]))]"
    ),
    "hints": [
        "Sort twice, least-significant key first.",
        "Use sorted(key=...) twice, reversing direction between passes.",
        "sorted(d.items(), key=lambda kv: kv[0], reverse=True) then sorted(..., key=lambda kv: int(kv[1])).",
    ],
    "test_cases": [
        {
            "name": "test_mixed_keys",
            "source": (
                "def test_mixed_keys():\n"
                "    assert solve({'a': '2', 'b': '1', 'c': '2'}) == "
                "[['b', '1'], ['c', '2'], ['a', '2']]"
            ),
        },
        {
            "name": "test_single_key",
            "source": ("def test_single_key():\n    assert solve({'x': '1'}) == [['x', '1']]"),
        },
    ],
}
