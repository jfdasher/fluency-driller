from drill.content.layout import dump_question_dir
from drill.content.manifest import build_import_array
from drill.content.schema import ContentQuestion, Test


def _write(
    root,
    name,
    *,
    topic="functions/closures",
    status="approved",
    canonical="def make(f):\n    return lambda x: x * f",
    source="def test_a():\n    assert make(3)(5) == 15",
):
    q = ContentQuestion(
        external_id=f"{topic}/{name}",
        topic=topic,
        kind="idiom",
        status=status,
        prompt="p",
        entry_point="make",
        canonical_answer=canonical,
        hints=["a", "b", "c"],
        tests=[Test(name="test_a", source=source)],
    )
    dump_question_dir(q, root / "python" / topic / name)


def test_build_emits_name_source_blob(tmp_path):
    _write(tmp_path, "factory")
    arr, errors, warnings = build_import_array(tmp_path)
    assert errors == []
    assert arr[0]["test_cases"] == [
        {"name": "test_a", "source": "def test_a():\n    assert make(3)(5) == 15"}
    ]


def test_build_rejects_canonical_that_fails_its_tests(tmp_path):
    _write(tmp_path, "broken", source="def test_a():\n    assert make(3)(5) == 999")
    arr, errors, warnings = build_import_array(tmp_path)
    assert arr == [] and any("fails its tests" in e for e in errors)


def test_build_skips_drafts(tmp_path):
    _write(tmp_path, "wip", status="draft")
    arr, errors, warnings = build_import_array(tmp_path)
    assert arr == [] and errors == []


def _write_approved_question(
    path,
    *,
    topic="groupby",
    name="sum-by-key",
    canonical="def make(f):\n    return lambda x: x * f",
    source="def test_a():\n    assert make(3)(5) == 15",
):
    q = ContentQuestion(
        external_id=f"{topic}/{name}",
        topic=topic,
        kind="idiom",
        status="approved",
        prompt="p",
        entry_point="make",
        canonical_answer=canonical,
        hints=["a", "b", "c"],
        tests=[Test(name="test_a", source=source)],
    )
    dump_question_dir(q, path)


def test_build_emits_corpus_object(tmp_path):
    from drill.content import manifest

    # lay out one approved question under <root>/pandas/<slug>/<name>/
    root = tmp_path / "content"
    _write_approved_question(root / "pandas" / "groupby" / "sum-by-key")
    arr, errors, warnings = manifest.build_import_array(root / "pandas")
    assert not errors
    assert arr
    assert all(q["corpus"] == "pandas" for q in arr)
