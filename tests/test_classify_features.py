"""Tests for scripts/classify_features.py — TDD, written before implementation."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import classify_features as cf

MINI_REF = {
    "meta": {"python_version": "3.x"},
    "keywords": ["if", "for"],
    "soft_keywords": ["match"],
    "builtins": {
        "functions": [{"name": "abs", "doc": "Return the abs."}],
        "types": [{"name": "int", "doc": "Integer type."}],
        "exceptions": [{"name": "ValueError", "doc": "Bad value."}],
        "constants": [{"name": "None", "doc": ""}],
    },
    "operators": [
        {"name": "add", "symbol": "+", "doc": "Same as a + b."},
        {"name": "attrgetter", "doc": "Return a callable object."},
    ],
    "type_methods": {
        "str": {
            "doc": "str(object='') -> str",
            "methods": [{"name": "split", "doc": "Return a list."}],
        },
        "list": {
            "doc": "Built-in mutable sequence.",
            "methods": [{"name": "append", "doc": "Append object."}],
        },
    },
}


# --- flatten_reference ---


def test_flatten_keywords():
    items = cf.flatten_reference(MINI_REF)
    kw_items = [x for x in items if x["kind"] == "keyword"]
    names = [x["item"] for x in kw_items]
    assert "if" in names
    assert "for" in names
    for kw in kw_items:
        assert kw["doc"] == ""


def test_flatten_soft_keywords():
    items = cf.flatten_reference(MINI_REF)
    sw_items = [x for x in items if x["kind"] == "soft keyword"]
    assert any(x["item"] == "match" for x in sw_items)


def test_flatten_builtin_kinds():
    items = cf.flatten_reference(MINI_REF)
    kinds = {x["kind"] for x in items}
    assert "builtin function" in kinds
    assert "builtin type" in kinds
    assert "builtin exception" in kinds
    assert "builtin constant" in kinds


def test_flatten_builtin_names():
    items = cf.flatten_reference(MINI_REF)
    assert any(x["item"] == "abs" and x["kind"] == "builtin function" for x in items)
    assert any(x["item"] == "ValueError" and x["kind"] == "builtin exception" for x in items)
    assert any(x["item"] == "None" and x["kind"] == "builtin constant" for x in items)


def test_flatten_type_methods_prefixed():
    items = cf.flatten_reference(MINI_REF)
    assert any(x["item"] == "str.split" and x["kind"] == "str method" for x in items)
    assert any(x["item"] == "list.append" and x["kind"] == "list method" for x in items)


def test_flatten_operators_use_symbol():
    items = cf.flatten_reference(MINI_REF)
    op_items = [x for x in items if x["kind"] == "operator"]
    assert any(x["item"] == "+" for x in op_items), "operator with symbol should use symbol as item"


def test_flatten_operators_no_symbol_use_name():
    items = cf.flatten_reference(MINI_REF)
    op_items = [x for x in items if x["kind"] == "operator"]
    assert any(x["item"] == "attrgetter" for x in op_items), (
        "operator without symbol should use name"
    )


def test_flatten_no_empty_items():
    items = cf.flatten_reference(MINI_REF)
    for entry in items:
        assert entry["item"], f"empty item string in {entry}"


def test_flatten_all_have_doc_key():
    items = cf.flatten_reference(MINI_REF)
    for entry in items:
        assert "doc" in entry, f"missing doc key in {entry}"
        assert isinstance(entry["doc"], str), f"doc must be str in {entry}"


# --- classify_batch ---


class _FakeContent:
    def __init__(self, text):
        self.text = text


class _FakeMessage:
    def __init__(self, text):
        self.content = [_FakeContent(text)]


class _FakeMessages:
    def __init__(self, response_text):
        self._resp = response_text

    def create(self, **kwargs):
        return _FakeMessage(self._resp)


class _FakeClient:
    def __init__(self, response_text):
        self.messages = _FakeMessages(response_text)


_SAMPLE_INPUT = [
    {"item": "str.split", "kind": "str method", "doc": "Return a list."},
]

_SAMPLE_RESPONSE = json.dumps(
    [
        {
            "item": "str.split",
            "kind": "str method",
            "disposition": "types/str-methods",
            "confidence": "high",
            "note": "",
        }
    ]
)


def test_classify_batch_returns_list():
    client = _FakeClient(_SAMPLE_RESPONSE)
    result = cf.classify_batch(client, _SAMPLE_INPUT)
    assert isinstance(result, list)
    assert len(result) == 1


def test_classify_batch_output_fields():
    client = _FakeClient(_SAMPLE_RESPONSE)
    result = cf.classify_batch(client, _SAMPLE_INPUT)
    row = result[0]
    for field in ("item", "kind", "disposition", "confidence"):
        assert field in row, f"missing field {field!r} in result row"
    assert row["confidence"] in ("high", "low")


def test_classify_batch_passes_items_to_model():
    """Verify the client receives the batch items in the user message."""
    captured = {}

    class _CapturingMessages:
        def create(self, **kwargs):
            captured.update(kwargs)
            return _FakeMessage(_SAMPLE_RESPONSE)

    class _CapturingClient:
        messages = _CapturingMessages()

    cf.classify_batch(_CapturingClient(), _SAMPLE_INPUT)
    user_msg = captured["messages"][0]["content"]
    assert "str.split" in user_msg, "batch item must appear in user message content"
