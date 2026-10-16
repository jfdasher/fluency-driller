"""Judgment of *intent* — did the answer demonstrate the target idiom?

A small `Judge` interface so the grader is swappable and the whole test suite
runs offline:

    Judge (ABC)
    ├── LLMJudge (ABC)         shared prompt-building + error translation
    │   └── AnthropicJudge     Anthropic SDK, structured output, pinned 5s budget
    └── DeterministicJudge     decides from self-reported test output (no network)

Leaves room for a future ``OpenAICompatJudge(LLMJudge)``.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel

from .models import Question, TestOutput

DEFAULT_MODEL = "claude-haiku-4-5"


class JudgeResult(BaseModel):
    """Structured grader output. ``verdict_proposal`` is authoritative;
    ``demonstrates_idiom`` is an advisory signal that is logged, not enforced."""

    verdict_proposal: Literal["pass", "fail"]
    demonstrates_idiom: bool
    hint_index: int | None = None
    comment: str = ""


class JudgeError(Exception):
    """Raised when the judge cannot produce a verdict (timeout, refusal,
    truncation, transport failure). The API maps this to HTTP 503 and logs
    nothing to ``events``."""


class Judge(ABC):
    """Grades one submission for a question."""

    @abstractmethod
    def judge(
        self,
        *,
        question: Question,
        answer_text: str,
        test_output: TestOutput | None,
    ) -> JudgeResult: ...


# --- DeterministicJudge -----------------------------------------------------


class DeterministicJudge(Judge):
    """Toy judge: a pass requires test output showing at least one pass and no
    failures. Tests-not-run (``test_output is None``) cannot confirm the idiom,
    so it fails. Used for the offline suite and curl-only demos."""

    def judge(
        self,
        *,
        question: Question,
        answer_text: str,
        test_output: TestOutput | None,
    ) -> JudgeResult:
        passed = test_output is not None and test_output.failed == 0 and test_output.passed > 0
        if passed:
            return JudgeResult(
                verdict_proposal="pass",
                demonstrates_idiom=True,
                comment="All self-reported tests passed.",
            )
        reason = "Tests were not run." if test_output is None else "Self-reported tests failed."
        return JudgeResult(
            verdict_proposal="fail",
            demonstrates_idiom=False,
            comment=reason,
        )


# --- LLMJudge ---------------------------------------------------------------

_SYSTEM_PROMPT = (
    "You are grading a programming drill. Decide whether the submitted answer "
    "DEMONSTRATES THE TARGET IDIOM, not merely whether it could pass tests. An "
    "answer that produces correct output via the wrong idiom (e.g. a hand-rolled "
    "comparison loop where the drill targets `sorted` with a key) is a FAIL with a "
    "hint pointing at the idiom. Return verdict_proposal ('pass'/'fail'), "
    "demonstrates_idiom (bool), an optional hint_index (the 0-based hint that best "
    "addresses the gap, or null), and a short comment."
)


class LLMJudge(Judge, ABC):
    """Shared machinery for LLM-backed judges: builds the prompt and translates
    any low-level failure into a ``JudgeError``. Subclasses implement ``_invoke``."""

    def judge(
        self,
        *,
        question: Question,
        answer_text: str,
        test_output: TestOutput | None,
    ) -> JudgeResult:
        user = self._build_user_prompt(question, answer_text, test_output)
        try:
            return self._invoke(_SYSTEM_PROMPT, user)
        except JudgeError:
            raise
        except Exception as exc:  # timeout, transport, parse, etc.
            raise JudgeError(str(exc)) from exc

    @staticmethod
    def _build_user_prompt(
        question: Question, answer_text: str, test_output: TestOutput | None
    ) -> str:
        if test_output is None:
            tests = "Tests were not run by the client."
        else:
            tests = (
                f"Self-reported tests: {test_output.passed} passed, {test_output.failed} failed."
            )
        hints = "\n".join(f"  [{i}] {h}" for i, h in enumerate(question.hints))
        return (
            f"Target idiom (topic): {question.topic}\n\n"
            f"Prompt:\n{question.prompt}\n\n"
            f"Canonical answer:\n{question.canonical_answer}\n\n"
            f"Submitted answer:\n{answer_text}\n\n"
            f"{tests}\n\n"
            f"Available hints (0-based):\n{hints}\n"
        )

    @abstractmethod
    def _invoke(self, system: str, user: str) -> JudgeResult: ...


class AnthropicJudge(LLMJudge):
    """Concrete LLM judge over the Anthropic API.

    Uses ``messages.parse`` with ``JudgeResult`` for schema-valid output, a small
    ``max_tokens``, and no thinking/effort params (unsupported on Haiku 4.5). The
    call pins a configurable timeout (``DRILL_JUDGE_TIMEOUT``, default 30 s) and
    disables SDK auto-retries so failures surface quickly — the SDK otherwise
    defaults to a 10-minute timeout with 2 retries.
    """

    def __init__(self, client=None, model: str | None = None, max_tokens: int = 1024):
        if client is None:
            import anthropic

            base_url = os.environ.get("ANTHROPIC_BASE_URL")
            client = anthropic.Anthropic(base_url=base_url) if base_url else anthropic.Anthropic()
        self._client = client
        self._model = model or os.environ.get("DRILL_MODEL", DEFAULT_MODEL)
        self._max_tokens = max_tokens
        self._timeout = float(os.environ.get("DRILL_JUDGE_TIMEOUT", "30.0"))

    def _invoke(self, system: str, user: str) -> JudgeResult:
        msg = self._client.with_options(timeout=self._timeout, max_retries=0).messages.parse(
            model=self._model,
            max_tokens=self._max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
            output_format=JudgeResult,
        )
        if getattr(msg, "stop_reason", None) in ("refusal", "max_tokens"):
            raise JudgeError(f"judge stopped early: {msg.stop_reason}")
        result = getattr(msg, "parsed_output", None)
        if result is None:
            raise JudgeError("judge returned no parseable output")
        return result


# --- factory ----------------------------------------------------------------


def build_judge() -> Judge:
    """Select the judge from ``DRILL_JUDGE`` (``anthropic`` | ``deterministic``)."""
    kind = os.environ.get("DRILL_JUDGE", "anthropic").lower()
    if kind == "deterministic":
        return DeterministicJudge()
    return AnthropicJudge()
