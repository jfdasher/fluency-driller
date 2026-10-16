"""One-time: convert content/python/**/<name>.yaml questions to directories.

Each old test case becomes an assert-based test:
  {input, expected} -> def test_case_i(): assert equal(<entry>(**input), expected)
  {input, check}    -> def test_case_i(): result = <entry>(**input); fn = <entry>; assert <check>
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from drill.content.layout import dump_question_dir
from drill.content.schema import ContentQuestion, Test


def _expected_source(i, entry, tc):
    return f"def test_case_{i}():\n    assert equal({entry}(**{tc['input']!r}), {tc['expected']!r})"


def _check_source(i, entry, tc):
    return (
        f"def test_case_{i}():\n"
        f"    result = {entry}(**{tc['input']!r})\n"
        f"    fn = {entry}\n"
        f"    assert {tc['check']}"
    )


def convert(data: dict) -> ContentQuestion:
    entry = data.get("entry_point", "solve")
    tests = []
    for i, tc in enumerate(data.get("test_cases", [])):
        if "check" in tc:
            src = _check_source(i, entry, tc)
        else:
            src = _expected_source(i, entry, tc)
        tests.append(Test(name=f"test_case_{i}", source=src))
    return ContentQuestion(
        external_id=data["external_id"],
        topic=data["topic"],
        language=data.get("language", "python"),
        modality=data.get("modality", "code"),
        kind=data["kind"],
        status=data.get("status", "draft"),
        prompt=data["prompt"],
        stub=data.get("stub"),
        entry_point=entry,
        canonical_answer=data["canonical_answer"],
        hints=list(data.get("hints", [])),
        tests=tests,
        provenance=data.get("provenance"),
    )


def main() -> int:
    root = Path("content/python")
    yamls = sorted(root.rglob("*.yaml"))
    for path in yamls:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        q = convert(data)
        qdir = path.with_suffix("")  # content/python/<slug>/<name>/
        dump_question_dir(q, qdir)
        path.unlink()
        print(f"migrated {path} -> {qdir}")
    print(f"migrated {len(yamls)} question(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
