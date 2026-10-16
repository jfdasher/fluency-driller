from __future__ import annotations

import json
import os
import re
import sys
from typing import Any

from .authoring_profiles import profile_for

DEFAULT_GEN_MODEL = "claude-sonnet-4-6"


class GeneratorError(Exception):
    """Raised when the model output cannot be parsed into candidate questions."""


CORE_SYSTEM_PROMPT = (
    "Return ONLY a JSON array (no prose, no markdown fences). Each element has: "
    "name (short kebab-case slug), prompt (one task statement), stub "
    "(a def with `...` body), entry_point (the function name), canonical_answer "
    "(idiomatic full function), hints (exactly 3, escalating helpful->strong->critical), "
    "tests. Each element of tests is {name: <kebab/snake test name>, source: <source code>} "
    "where source defines one `def test_*()` function that uses `assert` and PASSES when "
    "it raises no exception. The test constructs its own inputs and may call the entry_point "
    "by name (it is in scope) or via `fn` (the entry_point, injected). The canonical_answer "
    "MUST make every test pass. Keep tests small and exact. "
    "IMPORTANT: all values must be valid JSON (escape newlines in source as \\n)."
)


def system_prompt_for(corpus: str) -> str:
    return CORE_SYSTEM_PROMPT + "\n\n" + profile_for(corpus).system_section

_REPAIR_SYSTEM_PROMPT = (
    "You are a JSON repair assistant. "
    "YOU MUST RESPOND WITH ONLY A RAW JSON OBJECT. "
    "No prose, no reasoning, no analysis, no markdown fences, no explanation. "
    "Your entire response must be parseable by json.loads(). "
    "Start your response with '{' and end it with '}'."
)


def build_generation_prompt(
    *, slug: str, topic: str, kind: str, n: int, existing_ids: list[str],
    corpus: str = "python",
) -> str:
    existing = "\n".join(f"  - {e}" for e in existing_ids) or "  (none)"
    return (
        f"Corpus: {corpus}\n"
        f"Slug (topic field for every question): {slug}\n"
        f"Underlying question topic to drill: {topic}\n"
        f"Classification: {kind}\n"
        f"Produce exactly {n} distinct question(s).\n"
        f"Avoid duplicating these existing questions in this slug:\n{existing}\n"
    )


from .layout import dump_question_dir, load_question_dir  # for the CLI/tests
from .schema import ContentQuestion, Test
from .verify import verify_question


def _normalize_json_quirks(text: str) -> str:
    """Fix common LLM JSON generation quirks in a single char-by-char pass.

    Handles (in string context):
      - Literal control characters (\\n, \\r, \\t) → proper JSON escape sequences.
    Handles (outside string context):
      - Bare integer dict keys ({1: → {"1":) which Python allows but JSON does not.
    """
    result: list[str] = []
    in_string = False
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        if in_string:
            if ch == "\\" and i + 1 < n:
                result.append(text[i : i + 2])
                i += 2
            elif ch == '"':
                in_string = False
                result.append(ch)
                i += 1
            elif ch == "\n":
                result.append("\\n")
                i += 1
            elif ch == "\r":
                result.append("\\r")
                i += 1
            elif ch == "\t":
                result.append("\\t")
                i += 1
            else:
                result.append(ch)
                i += 1
        else:
            if ch == '"':
                in_string = True
                result.append(ch)
                i += 1
            elif ch in "{,":
                # Look ahead for bare integer key: whitespace* (-?digits) whitespace* :
                j = i + 1
                while j < n and text[j] in " \t\n\r":
                    j += 1
                k = j
                if k < n and text[k] == "-":
                    k += 1
                digit_start = k
                while k < n and text[k].isdigit():
                    k += 1
                digit_end = k
                if digit_end > digit_start:
                    m = digit_end
                    while m < n and text[m] in " \t":
                        m += 1
                    if m < n and text[m] == ":":
                        # Bare integer key — emit delimiter, whitespace, then quoted key
                        result.append(ch)
                        result.append(text[i + 1 : j])  # whitespace before key
                        result.append('"')
                        result.append(text[j:digit_end])  # the integer literal
                        result.append('"')
                        i = digit_end
                        continue
                result.append(ch)
                i += 1
            else:
                result.append(ch)
                i += 1

    return "".join(result)


def parse_candidates(raw: str) -> list[dict[str, Any]]:
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else ""
        text = text.rsplit("```", 1)[0]
    text = text.strip()
    # Fix common LLM JSON quirks: literal control chars in strings, bare int keys.
    text = _normalize_json_quirks(text)
    # Trailing commas before ] or } (applied after the char walk — safe on clean text).
    text = re.sub(r",\s*([}\]])", r"\1", text)
    try:
        # raw_decode parses the first complete JSON value and ignores any trailing
        # content (extra text, a second object, etc.) that json.loads would reject.
        data, _ = json.JSONDecoder().raw_decode(text)
    except json.JSONDecodeError as exc:
        print(f"[parse_candidates] raw output (first 1000 chars):\n{raw[:1000]}", file=sys.stderr)
        raise GeneratorError(f"could not parse model output as JSON: {exc}") from exc
    if isinstance(data, dict):  # repair returns a single object; wrap it
        return [data]
    if not isinstance(data, list):
        raise GeneratorError("model output was not a JSON array or object")
    return data


def assemble_question(
    *, slug: str, kind: str, candidate: dict[str, Any], existing_ids: set[str]
) -> ContentQuestion:
    """Turn a raw model candidate into a draft ContentQuestion with a unique id."""
    # Take only the last path segment — the model sometimes prefixes the slug.
    name = candidate["name"].split("/")[-1]
    external_id = f"{slug}/{name}"
    n = 2
    while external_id in existing_ids:
        external_id = f"{slug}/{name}-{n}"
        n += 1
    return ContentQuestion(
        external_id=external_id,
        topic=slug,
        kind=kind,
        status="draft",
        prompt=candidate["prompt"],
        stub=candidate.get("stub"),
        entry_point=candidate.get("entry_point", "solve"),
        canonical_answer=candidate["canonical_answer"],
        hints=list(candidate.get("hints", [])),
        tests=[Test(name=t["name"], source=t["source"])
               for t in candidate.get("tests", [])],
    )


class Generator:
    """Generates draft questions for a topic, verifying each and repairing failures."""

    def __init__(self, client=None, model: str | None = None, max_tokens: int = 4096):
        # Client is built lazily so Generator() is offline-safe (no API key needed
        # to construct it — only to actually call the model).
        self._client = client
        self._model = model or os.environ.get("DRILL_GEN_MODEL", DEFAULT_GEN_MODEL)
        self._max_tokens = max_tokens

    def _client_or_build(self):
        if self._client is None:
            import anthropic

            base_url = os.environ.get("ANTHROPIC_BASE_URL")
            self._client = (
                anthropic.Anthropic(base_url=base_url) if base_url else anthropic.Anthropic()
            )
        return self._client

    def _create(self, system: str, user: str) -> str:
        msg = self._client_or_build().messages.create(
            model=self._model, max_tokens=self._max_tokens,
            system=system, messages=[{"role": "user", "content": user}],
        )
        return msg.content[0].text

    def generate(
        self, *, slug: str, topic: str, kind: str, n: int,
        corpus: str = "python", existing_ids: list[str] | None = None,
        max_repair: int = 2,
    ) -> list[ContentQuestion]:
        existing = set(existing_ids or [])
        prompt = build_generation_prompt(
            slug=slug, topic=topic, kind=kind, n=n,
            existing_ids=sorted(existing), corpus=corpus,
        )
        candidates = parse_candidates(self._create(system_prompt_for(corpus), prompt))
        out: list[ContentQuestion] = []
        for cand in candidates:
            q = assemble_question(slug=slug, kind=kind, candidate=cand, existing_ids=existing)
            existing.add(q.external_id)
            q = self._verify_and_repair(q, topic=topic, max_repair=max_repair)
            out.append(q)
        return out

    def _verify_and_repair(
        self, q: ContentQuestion, *, topic: str, max_repair: int
    ) -> ContentQuestion:
        attempts = 1
        result = verify_question(q)
        while not result.ok and attempts <= max_repair:
            attempts += 1
            try:
                fixed = parse_candidates(
                    self._create(_REPAIR_SYSTEM_PROMPT, _repair_prompt(q, result.failures))
                )
            except GeneratorError:
                # Model returned prose instead of JSON; treat as exhausted repairs.
                break
            cand = fixed[0]
            q = q.model_copy(update={
                "canonical_answer": cand.get("canonical_answer", q.canonical_answer),
                "tests": [Test(name=t["name"], source=t["source"])
                          for t in cand.get("tests", [])] or q.tests,
            })
            result = verify_question(q)
        q.provenance = {
            "model": self._model,
            "source_topic": topic,
            "verified": {"ok": result.ok, "attempts": attempts, "failures": result.failures},
        }
        return q


import argparse
import sys
from pathlib import Path

import yaml


def _slug_dir(content_root: Path, corpus: str, slug: str) -> Path:
    return content_root / corpus / slug


def _existing_ids(content_root: Path, corpus: str, slug: str) -> list[str]:
    d = _slug_dir(content_root, corpus, slug)
    return [f"{slug}/{p.name}" for p in d.iterdir() if (p / "question.md").exists()] \
        if d.exists() else []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="drill-generate")
    parser.add_argument("slug")
    parser.add_argument("--corpus", default="python")
    parser.add_argument("--topics", default=None)
    parser.add_argument("--content-root", default="content")
    parser.add_argument("--topic", default=None, help="generate only this one topic")
    parser.add_argument("-n", type=int, default=2)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    content_root = Path(args.content_root)
    topics_path = args.topics or f"{args.content_root}/{args.corpus}/topics.yaml"
    topics_by_slug = yaml.safe_load(Path(topics_path).read_text(encoding="utf-8"))
    entries = topics_by_slug.get(args.slug, [])
    if args.topic:
        entries = [e for e in entries if e["topic"] == args.topic]
    if not entries:
        print(f"no topics for slug {args.slug!r}", file=sys.stderr)
        return 1

    generator = Generator()
    d = _slug_dir(content_root, args.corpus, args.slug)
    d.mkdir(parents=True, exist_ok=True)
    written = 0
    for entry in entries:
        existing = _existing_ids(content_root, args.corpus, args.slug)
        questions = generator.generate(
            slug=args.slug, topic=entry["topic"], kind=entry.get("kind", "idiom"),
            n=args.n, corpus=args.corpus, existing_ids=existing,
        )
        for q in questions:
            name = q.external_id.split("/")[-1]
            qdir = d / name
            if (qdir / "question.md").exists():  # resume: never overwrite
                continue
            dump_question_dir(q, qdir)
            written += 1
    print(f"wrote {written} question file(s) under {d}", file=sys.stderr)
    return 0


def _repair_prompt(q: ContentQuestion, failures: list[str]) -> str:
    return (
        "The following drill question FAILED verification — its canonical_answer "
        "does not satisfy its own tests. Return ONLY a single JSON object "
        "(same fields) with canonical_answer and tests corrected so they agree.\n\n"
        "Failures:\n" + "\n".join(f"  - {f}" for f in failures) + "\n\n"
        f"Question:\n{q.model_dump_json(indent=2)}\n"
    )
