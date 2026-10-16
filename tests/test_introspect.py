"""Tests for scripts/introspect_python.py — run before implementing."""

import os
import sys

# Allow importing from scripts/ as a module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import introspect_python as introspect


def get_ref():
    return introspect.build_reference()


# --- top-level structure ---


def test_top_level_sections():
    ref = get_ref()
    for key in ("meta", "keywords", "soft_keywords", "builtins", "operators", "type_methods"):
        assert key in ref, f"missing top-level key: {key!r}"


def test_meta_has_version_and_timestamp():
    meta = get_ref()["meta"]
    assert "python_version" in meta
    assert "generated_at" in meta
    assert meta["python_version"].startswith("3.")


# --- keywords ---


def test_keywords_non_empty():
    kw = get_ref()["keywords"]
    assert isinstance(kw, list)
    assert len(kw) > 0
    assert "if" in kw
    assert "for" in kw


def test_soft_keywords():
    skw = get_ref()["soft_keywords"]
    assert "match" in skw
    assert "case" in skw


# --- builtins ---


def test_builtins_has_four_categories():
    b = get_ref()["builtins"]
    for key in ("functions", "types", "exceptions", "constants"):
        assert key in b, f"missing builtins category: {key!r}"


def test_builtins_functions_contains_abs():
    funcs = get_ref()["builtins"]["functions"]
    names = [f["name"] for f in funcs]
    assert "abs" in names


def test_builtins_exceptions_contains_valueerror():
    excs = get_ref()["builtins"]["exceptions"]
    names = [e["name"] for e in excs]
    assert "ValueError" in names


def test_builtins_constants_contains_none():
    consts = get_ref()["builtins"]["constants"]
    names = [c["name"] for c in consts]
    assert "None" in names


# --- operators ---


def test_operators_non_empty():
    ops = get_ref()["operators"]
    assert isinstance(ops, list)
    assert len(ops) > 0


def test_operators_have_name_and_doc():
    for op in get_ref()["operators"]:
        assert "name" in op, f"operator entry missing 'name': {op}"
        assert "doc" in op, f"operator entry missing 'doc': {op}"
        assert isinstance(op["doc"], str)


def test_operator_add_has_symbol():
    ops = get_ref()["operators"]
    add = next((o for o in ops if o["name"] == "add"), None)
    assert add is not None, "'add' not found in operators"
    assert add.get("symbol") == "+", f"expected symbol '+', got {add.get('symbol')!r}"


# --- type_methods ---

EXPECTED_TYPES = (
    "str",
    "list",
    "dict",
    "tuple",
    "set",
    "frozenset",
    "bytes",
    "bytearray",
    "int",
    "float",
    "bool",
)


def test_type_methods_has_all_types():
    tm = get_ref()["type_methods"]
    for t in EXPECTED_TYPES:
        assert t in tm, f"missing type in type_methods: {t!r}"


def test_type_entries_have_doc_and_methods():
    tm = get_ref()["type_methods"]
    for t in EXPECTED_TYPES:
        entry = tm[t]
        assert "doc" in entry, f"{t} entry missing 'doc'"
        assert "methods" in entry, f"{t} entry missing 'methods'"
        assert isinstance(entry["doc"], str) and entry["doc"], f"{t} doc should be non-empty string"
        assert isinstance(entry["methods"], list)


def test_str_has_split_method():
    methods = get_ref()["type_methods"]["str"]["methods"]
    names = [m["name"] for m in methods]
    assert "split" in names


def test_list_has_append_method():
    methods = get_ref()["type_methods"]["list"]["methods"]
    names = [m["name"] for m in methods]
    assert "append" in names


def test_no_dunder_methods():
    for type_name, entry in get_ref()["type_methods"].items():
        for m in entry["methods"]:
            assert not m["name"].startswith("_"), (
                f"{type_name}: unexpected dunder method {m['name']!r}"
            )


def test_type_doc_is_multiline():
    doc = get_ref()["type_methods"]["str"]["doc"]
    assert "\n" in doc, "str type doc should span multiple lines (constructor signature)"


# --- doc field consistency ---


def test_all_doc_fields_are_strings():
    ref = get_ref()
    # builtins items
    for category in ref["builtins"].values():
        for item in category:
            assert isinstance(item.get("doc"), str), f"non-string doc in builtins: {item}"
    # operator items
    for op in ref["operators"]:
        assert isinstance(op.get("doc"), str), f"non-string doc in operator: {op}"
    # type method items
    for type_name, entry in ref["type_methods"].items():
        for m in entry["methods"]:
            assert isinstance(m.get("doc"), str), f"non-string doc in {type_name} method: {m}"
