"""Judge tests — all offline (no API key, no network)."""

import pytest

from drill.server.judge import (
    AnthropicJudge,
    DeterministicJudge,
    JudgeError,
    JudgeResult,
    LLMJudge,
    build_judge,
)
from drill.server.models import Question, TestOutput

Q = Question(
    id=1,
    topic="sorting/multi-key-stable",
    grader="python",
    modality="code",
    prompt="Sort it.",
    canonical_answer="def solve(d):\n    return sorted(d)",
    hints=["h0", "h1"],
    test_cases=[],
)


# --- DeterministicJudge -----------------------------------------------------


def test_deterministic_pass_when_tests_pass():
    r = DeterministicJudge().judge(
        question=Q, answer_text="x", test_output=TestOutput(passed=2, failed=0)
    )
    assert r.verdict_proposal == "pass"
    assert r.demonstrates_idiom is True


def test_deterministic_fail_when_tests_fail():
    r = DeterministicJudge().judge(
        question=Q, answer_text="x", test_output=TestOutput(passed=1, failed=1)
    )
    assert r.verdict_proposal == "fail"
    assert r.demonstrates_idiom is False
    assert r.hint_index is None  # server picks hint by hints_already_shown


def test_deterministic_fail_when_tests_not_run():
    r = DeterministicJudge().judge(question=Q, answer_text="x", test_output=None)
    assert r.verdict_proposal == "fail"


# --- LLMJudge shared machinery ---------------------------------------------


class StubLLMJudge(LLMJudge):
    def __init__(self, result=None, exc=None):
        self.result = result
        self.exc = exc
        self.captured = {}

    def _invoke(self, system: str, user: str) -> JudgeResult:
        self.captured = {"system": system, "user": user}
        if self.exc is not None:
            raise self.exc
        return self.result


def test_llmjudge_returns_invoke_result():
    res = JudgeResult(
        verdict_proposal="pass", demonstrates_idiom=True, hint_index=None, comment="ok"
    )
    out = StubLLMJudge(result=res).judge(question=Q, answer_text="a", test_output=None)
    assert out == res


def test_llmjudge_wraps_unexpected_errors_as_judgeerror():
    j = StubLLMJudge(exc=RuntimeError("boom"))
    with pytest.raises(JudgeError):
        j.judge(question=Q, answer_text="a", test_output=None)


def test_llmjudge_passes_through_judgeerror():
    j = StubLLMJudge(exc=JudgeError("refused"))
    with pytest.raises(JudgeError):
        j.judge(question=Q, answer_text="a", test_output=None)


def test_llmjudge_prompt_contains_key_fields():
    j = StubLLMJudge(
        result=JudgeResult(
            verdict_proposal="pass", demonstrates_idiom=True, hint_index=None, comment=""
        )
    )
    j.judge(question=Q, answer_text="MY_UNIQUE_ANSWER", test_output=TestOutput(passed=1))
    user = j.captured["user"]
    assert Q.topic in user
    assert Q.canonical_answer in user
    assert "MY_UNIQUE_ANSWER" in user


# --- AnthropicJudge with a fake SDK client ----------------------------------


class _FakeMessages:
    def __init__(self, msg):
        self._msg = msg
        self.calls = []

    def parse(self, **kwargs):
        self.calls.append(kwargs)
        return self._msg


class _FakeClient:
    def __init__(self, msg):
        self.messages = _FakeMessages(msg)
        self.opts = None

    def with_options(self, **kw):
        self.opts = kw
        return self


class _FakeMsg:
    def __init__(self, parsed=None, stop_reason="end_turn"):
        self.parsed_output = parsed
        self.stop_reason = stop_reason


def test_anthropic_judge_parses_and_pins_budget():
    res = JudgeResult(
        verdict_proposal="fail", demonstrates_idiom=False, hint_index=1, comment="loop"
    )
    client = _FakeClient(_FakeMsg(parsed=res, stop_reason="end_turn"))
    out = AnthropicJudge(client=client, model="claude-haiku-4-5").judge(
        question=Q, answer_text="a", test_output=None
    )
    assert out == res
    # 30s default timeout; auto-retries disabled
    assert client.opts == {"timeout": 30.0, "max_retries": 0}
    assert client.messages.calls[0]["model"] == "claude-haiku-4-5"


def test_anthropic_judge_refusal_raises_judgeerror():
    client = _FakeClient(_FakeMsg(parsed=None, stop_reason="refusal"))
    with pytest.raises(JudgeError):
        AnthropicJudge(client=client).judge(question=Q, answer_text="a", test_output=None)


def test_anthropic_judge_max_tokens_raises_judgeerror():
    res = JudgeResult(verdict_proposal="pass", demonstrates_idiom=True, hint_index=None, comment="")
    client = _FakeClient(_FakeMsg(parsed=res, stop_reason="max_tokens"))
    with pytest.raises(JudgeError):
        AnthropicJudge(client=client).judge(question=Q, answer_text="a", test_output=None)


# --- factory ----------------------------------------------------------------


def test_build_judge_selects_deterministic(monkeypatch):
    monkeypatch.setenv("DRILL_JUDGE", "deterministic")
    assert isinstance(build_judge(), DeterministicJudge)
