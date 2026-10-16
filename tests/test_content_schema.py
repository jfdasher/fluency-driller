from drill.content.schema import ContentQuestion, Test


def _q(**over):
    base = dict(
        external_id="t/x",
        topic="t",
        kind="idiom",
        prompt="p",
        canonical_answer="def solve():\n    return 1",
        entry_point="solve",
        hints=["a", "b", "c"],
        tests=[Test(name="test_one", source="def test_one():\n    assert solve() == 1")],
    )
    base.update(over)
    return ContentQuestion(**base)


def test_test_model_holds_name_and_source():
    t = Test(name="test_basic", source="def test_basic():\n    assert fn(2) == 4")
    assert t.name == "test_basic" and "assert" in t.source


def test_to_import_dict_emits_name_source_test_cases():
    q = _q()
    d = q.to_import_dict()
    assert d["test_cases"] == [
        {"name": "test_one", "source": "def test_one():\n    assert solve() == 1"}
    ]
    assert d["canonical_answer"] == "def solve():\n    return 1"


def test_content_question_defaults_tests_empty():
    q = _q(tests=[])
    assert q.tests == [] and q.to_import_dict()["test_cases"] == []
