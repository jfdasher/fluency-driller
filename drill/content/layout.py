"""Read/write a question as a directory of files.

Layout:
    <dir>/question.md          YAML frontmatter + "## Prompt" + "## Hints"
    <dir>/stub.py              skeleton shown to the user (optional)
    <dir>/canonical_answer.py  reference solution
    <dir>/tests/<name>.py      one assert-based test file each
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .schema import ContentQuestion, Test

_FRONTMATTER_KEYS = (
    "kind", "status", "topic", "entry_point", "grader", "modality", "provenance",
)


def dump_question_dir(q: ContentQuestion, dir: Path) -> None:
    dir = Path(dir)
    (dir / "tests").mkdir(parents=True, exist_ok=True)

    fm: dict[str, Any] = {
        "kind": q.kind, "status": q.status, "topic": q.topic,
        "entry_point": q.entry_point, "grader": q.grader, "modality": q.modality,
    }
    if q.provenance is not None:
        fm["provenance"] = q.provenance
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()

    hints = "\n".join(f"{i}. {h}" for i, h in enumerate(q.hints, start=1))
    body = f"---\n{fm_text}\n---\n## Prompt\n{q.prompt}\n\n## Hints\n{hints}\n"
    (dir / "question.md").write_text(body, encoding="utf-8")

    (dir / "stub.py").write_text((q.stub or "") + "\n", encoding="utf-8")
    (dir / "canonical_answer.py").write_text(q.canonical_answer.rstrip() + "\n",
                                             encoding="utf-8")
    for t in q.tests:
        (dir / "tests" / f"{t.name}.py").write_text(t.source.rstrip() + "\n",
                                                    encoding="utf-8")


def _parse_question_md(text: str) -> tuple[dict[str, Any], str, list[str]]:
    if not text.startswith("---"):
        raise ValueError("question.md missing YAML frontmatter")
    _, fm_text, body = text.split("---", 2)
    fm = yaml.safe_load(fm_text) or {}

    prompt_lines: list[str] = []
    hints: list[str] = []
    section = None
    for line in body.splitlines():
        if line.strip().lower() == "## prompt":
            section = "prompt"
            continue
        if line.strip().lower() == "## hints":
            section = "hints"
            continue
        if section == "prompt":
            prompt_lines.append(line)
        elif section == "hints":
            s = line.strip()
            if not s:
                continue
            # strip a leading "N." or "-" marker
            if s[0].isdigit():
                s = s.split(".", 1)[1].strip() if "." in s else s
            elif s.startswith("-"):
                s = s[1:].strip()
            hints.append(s)
    return fm, "\n".join(prompt_lines).strip(), hints


def load_question_dir(dir: Path) -> ContentQuestion:
    dir = Path(dir)
    fm, prompt, hints = _parse_question_md(
        (dir / "question.md").read_text(encoding="utf-8")
    )
    stub = (dir / "stub.py").read_text(encoding="utf-8").rstrip()
    canonical = (dir / "canonical_answer.py").read_text(encoding="utf-8").rstrip()
    tests = [
        Test(name=p.stem, source=p.read_text(encoding="utf-8").rstrip())
        for p in sorted((dir / "tests").glob("*.py"))
    ]
    external_id = f"{fm['topic']}/{dir.name}"
    return ContentQuestion(
        external_id=external_id, topic=fm["topic"], kind=fm["kind"],
        status=fm.get("status", "draft"), grader=fm.get("grader", "python"),
        modality=fm.get("modality", "code"), entry_point=fm.get("entry_point", "solve"),
        prompt=prompt, stub=stub or None, canonical_answer=canonical,
        hints=hints, tests=tests, provenance=fm.get("provenance"),
    )


def validate_question_dir(dir: Path) -> list[str]:
    problems: list[str] = []
    dir = Path(dir)
    try:
        q = load_question_dir(dir)
    except Exception as exc:  # noqa: BLE001 — report any load problem
        return [f"{dir}: load failed: {exc}"]
    if len(q.hints) != 3:
        problems.append(f"{dir}: expected exactly 3 hints, found {len(q.hints)}")
    if not q.prompt:
        problems.append(f"{dir}: missing or empty ## Prompt section")
    if not q.tests:
        problems.append(f"{dir}: no tests found")
    return problems
