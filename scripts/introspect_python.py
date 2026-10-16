"""Introspect the running Python interpreter and emit a structured JSON reference."""

import builtins as _builtins
import inspect
import json
import keyword
import operator
import sys
from datetime import UTC, datetime

SYMBOL_MAP = {
    "abs": "abs()",
    "add": "+",
    "and_": "&",
    "contains": "in",
    "eq": "==",
    "floordiv": "//",
    "ge": ">=",
    "getitem": "[]",
    "gt": ">",
    "invert": "~",
    "le": "<=",
    "lshift": "<<",
    "lt": "<",
    "matmul": "@",
    "mod": "%",
    "mul": "*",
    "ne": "!=",
    "neg": "-x",
    "not_": "not",
    "or_": "|",
    "pos": "+x",
    "pow": "**",
    "rshift": ">>",
    "sub": "-",
    "truediv": "/",
    "xor": "^",
}

INTROSPECTED_TYPES = (
    ("str", str),
    ("list", list),
    ("dict", dict),
    ("tuple", tuple),
    ("set", set),
    ("frozenset", frozenset),
    ("bytes", bytes),
    ("bytearray", bytearray),
    ("int", int),
    ("float", float),
    ("bool", bool),
)


def _first_line(text: str | None) -> str:
    if not text:
        return ""
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def _collect_keywords() -> tuple[list[str], list[str]]:
    return sorted(keyword.kwlist), sorted(keyword.softkwlist)


def _collect_builtins() -> dict:
    functions, types, exceptions, constants = [], [], [], []
    for name in sorted(dir(_builtins)):
        if name.startswith("_"):
            continue
        obj = getattr(_builtins, name)
        entry = {"name": name, "doc": _first_line(inspect.getdoc(obj))}
        if isinstance(obj, type) and issubclass(obj, BaseException):
            exceptions.append(entry)
        elif isinstance(obj, type):
            types.append(entry)
        elif callable(obj):
            functions.append(entry)
        else:
            constants.append(entry)
    return {
        "functions": functions,
        "types": types,
        "exceptions": exceptions,
        "constants": constants,
    }


def _collect_operators() -> list[dict]:
    ops = []
    for name in sorted(dir(operator)):
        if name.startswith("_"):
            continue
        fn = getattr(operator, name)
        if not callable(fn):
            continue
        entry: dict = {"name": name, "doc": _first_line(inspect.getdoc(fn))}
        if name in SYMBOL_MAP:
            entry["symbol"] = SYMBOL_MAP[name]
        ops.append(entry)
    return ops


def _collect_type_methods() -> dict:
    result = {}
    for type_name, type_obj in INTROSPECTED_TYPES:
        methods = []
        for attr_name in sorted(dir(type_obj)):
            if attr_name.startswith("_"):
                continue
            attr = getattr(type_obj, attr_name)
            if callable(attr):
                methods.append(
                    {
                        "name": attr_name,
                        "doc": _first_line(inspect.getdoc(attr)),
                    }
                )
        result[type_name] = {
            "doc": inspect.getdoc(type_obj) or "",
            "methods": methods,
        }
    return result


def build_reference() -> dict:
    kw, soft_kw = _collect_keywords()
    return {
        "meta": {
            "python_version": sys.version.split()[0],
            "generated_at": datetime.now(UTC).isoformat(),
        },
        "keywords": kw,
        "soft_keywords": soft_kw,
        "builtins": _collect_builtins(),
        "operators": _collect_operators(),
        "type_methods": _collect_type_methods(),
    }


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    default_out = str(__import__("pathlib").Path(__file__).parent / "python_reference.json")
    out_path = args[0] if args else default_out

    ref = build_reference()
    out = json.dumps(ref, indent=2, ensure_ascii=False)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
        f.write("\n")
    print(f"Written: {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
