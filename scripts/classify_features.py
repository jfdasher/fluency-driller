"""Classify Python language features from python_reference.json using Claude Haiku.

Usage:
    uv run python scripts/classify_features.py                # reads docs/python_reference.json
    uv run python scripts/classify_features.py ref.json out.json
"""

import json
import sys
from pathlib import Path

import anthropic

_SCRIPT_DIR = Path(__file__).parent
_DOCS_DIR = _SCRIPT_DIR.parent / "docs"

REFERENCE_PATH = _DOCS_DIR / "python_reference.json"
COVERAGE_PATH = _DOCS_DIR / "coverage.json"
BATCH_SIZE = 5

_SYSTEM_PROMPT = """\
You are classifying Python language items into a fixed topic taxonomy for a
fluency-drill question store. The audience is a rusty professional programmer
drilling for recall speed, not a beginner learning concepts.

For each item below, assign exactly one disposition:

1. A topic slug from the CLOSED vocabulary below. Choose the most specific
   applicable slug. You may not invent slugs.
2. "deferred:<short reason>" — in-scope for the language, out of scope for v1
   (e.g., async, concurrency, packaging).
3. "not-drillable:<short reason>" — nothing a professional would ever need to
   recall under time pressure (internal machinery, REPL easter eggs,
   interactive-only helpers).

Rules:
- An item used weekly by working Python programmers must map to a slug, not a
  bucket. When torn between two slugs, prefer the one whose chapter owns the
  *recall task* (e.g., `sorted` belongs to iteration/sorting, not
  builtins/misc, because the drillable skill is key-function fluency).
- Set "confidence" to "low" whenever you are torn between dispositions or the
  item is genuinely ambiguous. Low-confidence rows go to human review; do not
  guess confidently.
- Output a JSON array only. No prose, no markdown fences.

Output schema, one object per input item:
{"item": str, "kind": str, "disposition": str, "confidence": "high"|"low",
 "note": str}   // note: one line, only when it earns its place

SLUG VOCABULARY:
syntax/f-strings, syntax/string-literals, syntax/numeric-literals,
syntax/annotations, types/str-methods, types/list, types/dict, types/set,
types/tuple, types/numeric, types/bytes, operators/comparison,
operators/boolean, operators/walrus, operators/unpacking, operators/ternary,
operators/bitwise, operators/precedence, control-flow/for, control-flow/while,
control-flow/with, control-flow/match, control-flow/loop-control,
comprehensions/basic, comprehensions/multi-clause, comprehensions/filtering,
comprehensions/generator-exprs, comprehensions/nested, functions/signatures,
functions/defaults, functions/lambda, functions/closures,
functions/decorators-use, functions/decorators-write, functions/generators,
functions/first-class, classes/basics, classes/dunder-repr-eq,
classes/dunder-container, classes/dunder-operators, classes/properties,
classes/dataclasses, classes/inheritance, classes/slots, classes/descriptors,
classes/metaclasses, errors/handling, errors/raising, errors/eafp,
errors/builtin-hierarchy, iteration/protocol, iteration/builtins,
iteration/sorting, iteration/exhaustion, gotchas/mutable-defaults,
gotchas/late-binding, gotchas/identity, gotchas/copy, gotchas/scoping,
gotchas/truthiness, gotchas/aliasing, gotchas/evaluation-order,
builtins/any-all, builtins/map-filter, builtins/introspection,
builtins/conversion, builtins/io, builtins/misc, stdlib/collections,
stdlib/itertools, stdlib/functools, stdlib/re, stdlib/pathlib, stdlib/json,
stdlib/datetime, stdlib/contextlib, stdlib/os-sys, stdlib/logging,
stdlib/string-tools, stdlib/heapq-bisect, typing/basics, typing/structural,
typing/generics, modules/imports, modules/main\
"""


def flatten_reference(data: dict) -> list[dict]:
    items: list[dict] = []

    for kw in data.get("keywords", []):
        items.append({"item": kw, "kind": "keyword", "doc": ""})

    for sw in data.get("soft_keywords", []):
        items.append({"item": sw, "kind": "soft keyword", "doc": ""})

    builtins = data.get("builtins", {})
    for entry in builtins.get("functions", []):
        items.append(
            {"item": entry["name"], "kind": "builtin function", "doc": entry.get("doc", "")}
        )
    for entry in builtins.get("types", []):
        items.append({"item": entry["name"], "kind": "builtin type", "doc": entry.get("doc", "")})
    for entry in builtins.get("exceptions", []):
        items.append(
            {"item": entry["name"], "kind": "builtin exception", "doc": entry.get("doc", "")}
        )
    for entry in builtins.get("constants", []):
        items.append(
            {"item": entry["name"], "kind": "builtin constant", "doc": entry.get("doc", "")}
        )

    for entry in data.get("operators", []):
        item_name = entry.get("symbol") or entry["name"]
        items.append({"item": item_name, "kind": "operator", "doc": entry.get("doc", "")})

    for type_name, type_entry in data.get("type_methods", {}).items():
        for method in type_entry.get("methods", []):
            items.append(
                {
                    "item": f"{type_name}.{method['name']}",
                    "kind": f"{type_name} method",
                    "doc": method.get("doc", ""),
                }
            )

    return items


def classify_batch(client, items: list[dict]) -> list[dict]:
    user_content = "ITEMS:\n" + json.dumps(items, ensure_ascii=False)

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2048,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )

    raw = message.content[0].text.strip()
    # Strip markdown fences the model sometimes adds despite instructions
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]  # drop opening fence line
        raw = raw.rsplit("```", 1)[0]  # drop closing fence
    return json.loads(raw.strip())


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    ref_path = Path(args[0]) if args else REFERENCE_PATH
    out_path = Path(args[1]) if len(args) > 1 else COVERAGE_PATH

    ref = json.loads(ref_path.read_text(encoding="utf-8"))
    all_items = flatten_reference(ref)

    existing: dict[str, dict] = {}
    if out_path.exists():
        try:
            for row in json.loads(out_path.read_text(encoding="utf-8")):
                existing[row["item"]] = row
        except (json.JSONDecodeError, KeyError):
            pass

    client = anthropic.Anthropic()
    results: list[dict] = list(existing.values())
    todo = [item for item in all_items if item["item"] not in existing]

    for i in range(0, len(todo), BATCH_SIZE):
        batch = todo[i : i + BATCH_SIZE]
        print(f"Classifying {i + 1}–{i + len(batch)} / {len(todo)}...", file=sys.stderr)
        classified = classify_batch(client, batch)
        results.extend(classified)
        out_path.write_text(
            json.dumps(results, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    print(f"Done: {len(results)} items written to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
