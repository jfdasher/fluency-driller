from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .layout import load_question_dir
from .verify import verify_question


def iter_question_dirs(corpus_root: str | Path):
    """Yield (path, corpus, ContentQuestion | Exception) for every question directory.

    corpus_root is the corpus directory itself (e.g. content/python); the
    corpus name is derived from its final path component. A question
    directory is any dir under corpus_root/** that contains a question.md
    file.
    """
    root = Path(corpus_root)
    corpus = root.name
    for md in sorted(root.rglob("question.md")):
        path = md.parent
        try:
            q = load_question_dir(path)
            yield path, corpus, q
        except Exception as exc:  # noqa: BLE001 — report load failures as errors
            yield path, corpus, exc


def build_import_array(
    content_root: str | Path, approved_only: bool = True
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    """Return (import_array, errors, warnings). Errors block; warnings inform."""
    root = Path(content_root)
    errors: list[str] = []
    warnings: list[str] = []
    seen: dict[str, Path] = {}
    out: list[dict[str, Any]] = []

    for path, corpus, q in iter_question_dirs(root):
        if isinstance(q, Exception):
            errors.append(f"{path}: schema error: {q}")
            continue
        if q.external_id in seen:
            errors.append(
                f"duplicate external_id {q.external_id!r}: {path} and {seen[q.external_id]}"
            )
        seen[q.external_id] = path

        # dir/topic coherence: <corpus_root>/<slug>/<name>/
        slug_from_path = path.parent.relative_to(root).as_posix()
        if slug_from_path != q.topic:
            warnings.append(
                f"{q.external_id}: dir slug {slug_from_path!r} != topic {q.topic!r}"
            )

        if approved_only and q.status != "approved":
            continue

        # Re-verify at build time: human review may have edited canonical_answer
        # after generation, staleing provenance.verified.
        result = verify_question(q)
        if not result.ok:
            errors.append(f"{q.external_id}: canonical answer fails its tests: {result.failures}")
            continue

        d = q.to_import_dict()
        d["corpus"] = corpus
        out.append(d)

    return out, errors, warnings


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not (1 <= len(args) <= 2):
        print("usage: drill-build-manifest <corpus_content_dir> [out.json]", file=sys.stderr)
        return 2
    content_root = args[0]
    corpus = Path(content_root).name
    out_path = Path(args[1]) if len(args) > 1 else Path(content_root) / "manifest.json"
    arr, errors, warnings = build_import_array(content_root)
    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    out_path.write_text(
        json.dumps({"corpus": corpus, "questions": arr}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(arr)} question(s) to {out_path}", file=sys.stderr)
    return 0
