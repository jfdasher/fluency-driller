import pytest

from drill.content.generator import (
    GeneratorError,
    build_generation_prompt,
    parse_candidates,
)


def test_prompt_contains_topic_slug_kind_and_existing_names():
    p = build_generation_prompt(
        slug="iteration/sorting",
        topic="double sort with lambda as key",
        kind="idiom",
        n=2,
        existing_ids=["iteration/sorting/by-abs"],
    )
    assert "iteration/sorting" in p
    assert "double sort with lambda as key" in p
    assert "idiom" in p
    assert "2" in p
    assert "by-abs" in p  # novelty context


def test_parse_candidates_handles_plain_json():
    raw = '[{"name": "x", "prompt": "p", "canonical_answer": "def solve():\\n    return 1", "hints": ["a","b","c"], "tests": [{"name": "test_basic", "source": "def test_basic():\\n    assert solve() == 1"}]}]'
    out = parse_candidates(raw)
    assert out[0]["name"] == "x"


def test_parse_candidates_strips_markdown_fences():
    raw = '```json\n[{"name": "x"}]\n```'
    assert parse_candidates(raw) == [{"name": "x"}]


def test_parse_candidates_wraps_bare_object():
    # The repair prompt asks for a single object; accept it as a 1-element list.
    assert parse_candidates('{"name": "x"}') == [{"name": "x"}]


def test_parse_candidates_raises_on_garbage():
    with pytest.raises(GeneratorError):
        parse_candidates("not json at all")


def test_parse_candidates_strips_trailing_commas():
    raw = '[{"name": "x",}]'
    assert parse_candidates(raw) == [{"name": "x"}]


def test_parse_candidates_escapes_literal_newlines_in_strings():
    # LLM emits a real 0x0A inside a JSON string value instead of \n.
    raw = '[{"code": "def solve():\n    return 1"}]'
    result = parse_candidates(raw)
    assert result[0]["code"] == "def solve():\n    return 1"


def test_parse_candidates_quotes_bare_integer_dict_keys():
    # LLM emits Python-style dict keys {1: 3, 2: 2} which are invalid JSON.
    raw = '[{"expected": {1: 3, 2: 2, 3: 1}}]'
    result = parse_candidates(raw)
    assert result[0]["expected"] == {"1": 3, "2": 2, "3": 1}


def test_parse_candidates_integer_keys_inside_string_not_quoted():
    # Integer-looking keys inside a string value must NOT be touched.
    raw = '[{"code": "d = {1: 2}"}]'
    result = parse_candidates(raw)
    assert result[0]["code"] == "d = {1: 2}"


def test_parse_candidates_ignores_trailing_content():
    # Repair prompt may return an object followed by extra text or a second object.
    raw = '{"name": "x"}\n\nSome explanation text.'
    assert parse_candidates(raw) == [{"name": "x"}]


from drill.content.generator import assemble_question
from drill.content.schema import ContentQuestion

_CAND = {
    "name": "char-frequency",
    "prompt": "Count chars.",
    "stub": "def solve(s):\n    ...",
    "entry_point": "solve",
    "canonical_answer": "def solve(s):\n    return {}",
    "hints": ["a", "b", "c"],
    "tests": [{"name": "test_basic", "source": "def test_basic():\n    assert solve('x') == {}"}],
}


def test_assemble_sets_ids_topic_kind_and_status():
    q = assemble_question(slug="types/dict", kind="idiom", candidate=_CAND, existing_ids=set())
    assert isinstance(q, ContentQuestion)
    assert q.external_id == "types/dict/char-frequency"
    assert q.topic == "types/dict"
    assert q.kind == "idiom"
    assert q.status == "draft"


def test_assemble_dedupes_name_against_existing():
    q = assemble_question(
        slug="types/dict",
        kind="idiom",
        candidate=_CAND,
        existing_ids={"types/dict/char-frequency"},
    )
    assert q.external_id == "types/dict/char-frequency-2"


def test_assemble_strips_path_prefix_from_name():
    # Model sometimes returns "types/dict/char-frequency" instead of "char-frequency".
    cand = {**_CAND, "name": "types/dict/char-frequency"}
    q = assemble_question(slug="types/dict", kind="idiom", candidate=cand, existing_ids=set())
    assert q.external_id == "types/dict/char-frequency"  # not "types/dict/types/dict/..."


import json as _json

from drill.content.generator import Generator


class _Block:
    def __init__(self, text):
        self.text = text


class _Msg:
    def __init__(self, text):
        self.content = [_Block(text)]


class _Messages:
    def __init__(self, queue):
        self._queue = list(queue)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _Msg(self._queue.pop(0))


class _StubClient:
    def __init__(self, queue):
        self.messages = _Messages(queue)


_GOOD = {
    "name": "upper",
    "prompt": "Upper.",
    "stub": "def solve(s):\n    ...",
    "entry_point": "solve",
    "canonical_answer": "def solve(s):\n    return s.upper()",
    "hints": ["a", "b", "c"],
    "tests": [
        {"name": "test_basic", "source": "def test_basic():\n    assert solve('ab') == 'AB'"}
    ],
}
_BAD = {**_GOOD, "canonical_answer": "def solve(s):\n    return s"}  # fails its test


def test_generate_returns_verified_question():
    client = _StubClient([_json.dumps([_GOOD])])
    qs = Generator(client=client).generate(
        slug="types/str-methods", topic="upper", kind="recall", n=1
    )
    assert len(qs) == 1
    assert qs[0].provenance["verified"]["ok"] is True


def test_generate_repairs_a_failing_candidate():
    # First batch yields a broken candidate; repair call returns the fixed one.
    client = _StubClient([_json.dumps([_BAD]), _json.dumps(_GOOD)])
    qs = Generator(client=client).generate(
        slug="types/str-methods", topic="upper", kind="recall", n=1, max_repair=1
    )
    assert qs[0].provenance["verified"]["ok"] is True
    assert qs[0].provenance["verified"]["attempts"] == 2


def test_generate_flags_unrepairable_candidate():
    client = _StubClient([_json.dumps([_BAD]), _json.dumps(_BAD)])
    qs = Generator(client=client).generate(
        slug="types/str-methods", topic="upper", kind="recall", n=1, max_repair=1
    )
    assert qs[0].status == "draft"
    assert qs[0].provenance["verified"]["ok"] is False
    assert qs[0].provenance["verified"]["failures"]


def test_generate_handles_prose_repair_response():
    # Repair call returns prose instead of JSON; should degrade gracefully, not crash.
    client = _StubClient([_json.dumps([_BAD]), "Looking at the failures:\nThe test expects..."])
    qs = Generator(client=client).generate(
        slug="types/str-methods", topic="upper", kind="recall", n=1, max_repair=1
    )
    assert qs[0].provenance["verified"]["ok"] is False  # failed, but no exception


import drill.content.generator as gen


def test_parse_candidates_keeps_name_source_tests():
    raw = (
        '[{"name": "factory", "prompt": "p", "stub": "def make(f):\\n    ...",'
        ' "entry_point": "make",'
        ' "canonical_answer": "def make(f):\\n    return lambda x: x*f",'
        ' "hints": ["a", "b", "c"],'
        ' "tests": [{"name": "test_basic",'
        ' "source": "def test_basic():\\n    assert make(3)(5) == 15"}]}]'
    )
    cands = gen.parse_candidates(raw)
    assert cands[0]["tests"][0]["name"] == "test_basic"


def test_assemble_question_builds_tests():
    candidate = {
        "name": "factory",
        "prompt": "p",
        "stub": "def make(f):\n    ...",
        "entry_point": "make",
        "canonical_answer": "def make(f):\n    return lambda x: x*f",
        "hints": ["a", "b", "c"],
        "tests": [
            {"name": "test_basic", "source": "def test_basic():\n    assert make(3)(5) == 15"}
        ],
    }
    q = gen.assemble_question(
        slug="functions/closures",
        kind="idiom",
        candidate=candidate,
        existing_ids=set(),
    )
    assert q.tests[0].name == "test_basic"
    assert "assert make(3)(5) == 15" in q.tests[0].source


def _topic_file(tmp_path):
    p = tmp_path / "topics.yaml"
    p.write_text("types/str-methods:\n  - topic: upper\n    kind: recall\n", encoding="utf-8")
    return p


def _stub_generate(monkeypatch):
    def fake_generate(
        self, *, slug, topic, kind, n, corpus="python", existing_ids=None, max_repair=2
    ):
        return [
            ContentQuestion(
                external_id=f"{slug}/upper",
                topic=slug,
                kind=kind,
                status="draft",
                prompt="Upper.",
                canonical_answer="def solve(s):\n    return s.upper()",
                hints=["a", "b", "c"],
            )
        ]

    monkeypatch.setattr(gen.Generator, "generate", fake_generate)


def test_main_writes_question_files(tmp_path, monkeypatch):
    _stub_generate(monkeypatch)
    tf = _topic_file(tmp_path)
    rc = gen.main(
        ["types/str-methods", "--topics", str(tf), "--content-root", str(tmp_path), "-n", "1"]
    )
    assert rc == 0
    assert (tmp_path / "python" / "types/str-methods" / "upper" / "question.md").exists()


def test_main_resume_skips_existing(tmp_path, monkeypatch):
    _stub_generate(monkeypatch)
    tf = _topic_file(tmp_path)
    # Pre-create the target directory; generate must not overwrite it.
    d = tmp_path / "python" / "types/str-methods"
    d.mkdir(parents=True)
    existing = ContentQuestion(
        external_id="types/str-methods/upper",
        topic="types/str-methods",
        kind="recall",
        status="approved",
        prompt="x",
        canonical_answer="def solve(s):\n    return s",
    )
    gen.dump_question_dir(existing, d / "upper")
    rc = gen.main(
        ["types/str-methods", "--topics", str(tf), "--content-root", str(tmp_path), "-n", "1"]
    )
    assert rc == 0
    assert gen.load_question_dir(d / "upper").status == "approved"  # untouched


def test_generate_writes_under_corpus_dir(tmp_path, monkeypatch):
    def fake_generate(
        self, *, slug, topic, kind, n, corpus="python", existing_ids=None, max_repair=2
    ):
        return [
            ContentQuestion(
                external_id=f"{slug}/sum-by-key",
                topic=slug,
                kind=kind,
                status="draft",
                prompt="Sum by key.",
                canonical_answer="def solve(rows):\n    return {}",
                hints=["a", "b", "c"],
            )
        ]

    monkeypatch.setattr(gen.Generator, "generate", fake_generate)

    (tmp_path / "pandas").mkdir(parents=True)
    (tmp_path / "pandas" / "topics.yaml").write_text(
        "groupby:\n  - topic: sum by key\n    kind: idiom\n", encoding="utf-8"
    )
    rc = gen.main(["groupby", "--corpus", "pandas", "--content-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / "pandas" / "groupby" / "sum-by-key" / "question.md").exists()


from drill.content.authoring_profiles import profile_for
from drill.content.generator import system_prompt_for


def test_profile_for_known_and_unknown_corpora():
    assert profile_for("pandas").name == "pandas"
    assert profile_for("python").name == "python"
    # unknown corpus falls back to the python profile
    assert profile_for("klingon").name == "python"


def test_python_section_has_legacy_instructions():
    s = profile_for("python").system_section
    assert "atomic Python drill questions" in s
    assert "equal(a, b)" in s
    assert "make_multiplier" in s
    assert "deep_copy" in s


def test_pandas_section_has_hybrid_contract_and_rendering():
    s = profile_for("pandas").system_section
    assert "assert_frame_equal" in s
    assert "import pandas as pd" in s
    assert "NATURAL return type" in s  # scalar/Series answers not forced into a DataFrame
    assert "np.testing.assert_array_equal" in s  # numpy-foundations returns ndarrays, not wrapped
    # never route pandas equality through equal()
    assert "equal(a, b)" not in s or "NEVER use `equal(a, b)`" in s
    # monospace DataFrame rendering directive
    assert "monospace" in s
    assert "df.columns" in s


def test_system_prompt_python_is_behavior_equivalent():
    p = system_prompt_for("python")
    # core schema invariants
    assert "Return ONLY a JSON array" in p
    assert "hints (exactly 3" in p
    assert "escape newlines" in p
    # legacy python specifics preserved
    assert "atomic Python drill questions" in p
    assert "equal(a, b)" in p
    assert "make_multiplier" in p


def test_system_prompt_pandas_carries_contract():
    p = system_prompt_for("pandas")
    assert "Return ONLY a JSON array" in p  # shares the core
    assert "assert_frame_equal" in p  # pandas contract
    assert "monospace" in p  # rendering directive


def test_build_generation_prompt_includes_corpus():
    p = build_generation_prompt(
        slug="index/reindex-align",
        topic="align two series",
        kind="idiom",
        n=1,
        existing_ids=[],
        corpus="pandas",
    )
    assert "pandas" in p


def test_generate_uses_corpus_system_prompt():
    client = _StubClient([_json.dumps([_GOOD])])
    Generator(client=client).generate(
        slug="index/reindex-align",
        topic="align",
        kind="idiom",
        n=1,
        corpus="pandas",
    )
    system_sent = client.messages.calls[0]["system"]
    assert "assert_frame_equal" in system_sent
