"""Tests for the Neovim sidecar core — offline, no live server."""

import json

import httpx

from drill.client.nvim_host import NeovimShell, NvimDrillClient

QUESTION = {
    "question_id": 7,
    "topic": "iteration/sorting",
    "grader": "python",
    "modality": "code",
    "prompt": "Sort it.",
    "stub": "def solve(lst):\n    ...",
    "entry_point": "solve",
    "hints_total": 2,
    "due_count": 1,
    "new_count": 4,
    "test_cases": [
        {"name": "test_a", "source": "def test_a():\n    assert solve([3, 1, 2]) == [1, 2, 3]"},
        {"name": "test_b", "source": "def test_b():\n    assert solve([1]) == [1]"},
    ],
}


def _make_client(handler=None, now=None):
    effects = []

    def send(eff):
        effects.append(eff)

    shell = NeovimShell(send=send)
    if handler:
        http = httpx.Client(transport=httpx.MockTransport(handler))
    else:
        http = httpx.Client(
            transport=httpx.MockTransport(lambda r: httpx.Response(200, json=QUESTION))
        )
    ticks = iter(now or [1.0, 5.0])
    client = NvimDrillClient(
        "http://test",
        "anon",
        shell=shell,
        http=http,
        now=lambda: next(ticks),
    )
    return client, effects


def _next_handler(r):
    return httpx.Response(200, json=QUESTION)


# --- NeovimShell -----------------------------------------------------------


def test_neovim_shell_set_next_input_emits_set_buffer():
    effects = []
    shell = NeovimShell(send=effects.append)
    shell.set_next_input("def solve(lst):\n    pass")
    assert effects == [{"effect": "set_buffer", "text": "def solve(lst):\n    pass"}]


# --- NvimDrillClient.do_test_from_source -----------------------------------


def test_do_test_from_source_all_pass():
    client, _ = _make_client()
    client.do_next()
    result = client.do_test_from_source("def solve(lst):\n    return sorted(lst)")
    assert result["passed"] == 2
    assert result["failed"] == 0
    assert client.state["test_output"]["passed"] == 2


def test_do_test_from_source_partial_fail():
    client, _ = _make_client()
    client.do_next()
    result = client.do_test_from_source("def solve(lst):\n    return lst")
    assert result["failed"] > 0


def test_do_test_from_source_normalizes_tuples():
    client, _ = _make_client()
    client.state = {
        "entry_point": "solve",
        "test_cases": [
            {
                "name": "test_a",
                "source": "def test_a():\n    assert equal(solve([3, 1, 2]), [1, 2, 3])",
            }
        ],
    }
    result = client.do_test_from_source("def solve(lst):\n    return tuple(sorted(lst))")
    assert result["failed"] == 0


def test_do_test_from_source_missing_entry_point():
    client, _ = _make_client()
    client.do_next()
    result = client.do_test_from_source("x = 1")
    assert result["failed"] > 0
    assert "NameError" in result["detail"][0]["reason"]


def test_do_test_from_source_timeout(monkeypatch):
    import subprocess

    def _raise(*a, **kw):
        raise subprocess.TimeoutExpired(cmd="python", timeout=0.001)

    monkeypatch.setattr(subprocess, "run", _raise)
    client, _ = _make_client()
    client.do_next()
    result = client.do_test_from_source("def solve(lst): pass")
    assert "error" in result
    assert "timeout" in result["error"]


def test_do_test_from_source_no_active_question():
    client, _ = _make_client()
    result = client.do_test_from_source("def solve(lst): return sorted(lst)")
    assert "error" in result


def test_do_test_from_source_runs_assert_tests():
    client, _ = _make_client()
    client.state = {
        "entry_point": "make",
        "test_cases": [{"name": "test_a", "source": "def test_a():\n    assert make(3)(5) == 15"}],
    }
    result = client.do_test_from_source("def make(f):\n    return lambda x: x * f")
    assert result["passed"] == 1 and result["failed"] == 0


def test_do_test_from_source_reports_failure_reason():
    client, _ = _make_client()
    client.state = {
        "entry_point": "make",
        "test_cases": [{"name": "test_a", "source": "def test_a():\n    assert make(3)(5) == 999"}],
    }
    result = client.do_test_from_source("def make(f):\n    return lambda x: x * f")
    assert result["failed"] == 1
    assert "AssertionError" in result["detail"][0]["reason"]


# --- NvimDrillClient.do_submit_from_source ---------------------------------


def test_do_submit_from_source_pass():
    def handler(r):
        if r.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(
            200,
            json={
                "verdict": "pass",
                "question_id": 7,
                "hint": None,
                "hint_index": None,
                "judge_comment": "ok",
            },
        )

    client, _ = _make_client(handler=handler)
    client.do_next()
    outcome = client.do_submit_from_source("def solve(lst):\n    return sorted(lst)")
    assert outcome["outcome"] == "submitted"
    assert "pass" in outcome["verdict"]
    assert client.state is None


def test_do_submit_from_source_blocked_when_tests_fail():
    posted = {"n": 0}

    def handler(r):
        if r.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        posted["n"] += 1
        return httpx.Response(
            200,
            json={
                "verdict": "pass",
                "question_id": 7,
                "hint": None,
                "hint_index": None,
                "judge_comment": "ok",
            },
        )

    client, _ = _make_client(handler=handler)
    client.do_next()
    outcome = client.do_submit_from_source("def solve(lst):\n    return lst")  # unsorted
    assert outcome["outcome"] == "tests_failed"
    assert outcome["tests"]["failed"] > 0
    assert posted["n"] == 0  # never POSTed


def test_do_submit_from_source_idiom_fail_after_tests_pass():
    def handler(r):
        if r.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(
            200,
            json={
                "verdict": "fail",
                "question_id": 7,
                "hint": "use sorted()",
                "hint_index": 0,
                "judge_comment": "wrong",
            },
        )

    client, _ = _make_client(handler=handler, now=[1.0, 2.0])
    client.do_next()
    # tests pass, but the judge returns an idiom fail+hint — still recorded
    outcome = client.do_submit_from_source("def solve(lst):\n    return sorted(lst)")
    assert outcome["outcome"] == "submitted"
    assert "sorted" in outcome["verdict"]


def test_do_submit_from_source_no_state():
    client, _ = _make_client()
    outcome = client.do_submit_from_source("def solve(lst): return sorted(lst)")
    assert outcome["outcome"] == "no_state"
    assert "no active" in outcome["message"].lower()


# --- NvimHost dispatch ---------------------------------------------------------

from drill.client.nvim_host import NvimHost


def _make_host(handler=None, now=None):
    effects = []

    def send(eff):
        effects.append(eff)

    shell = NeovimShell(send=send)
    if handler:
        http = httpx.Client(transport=httpx.MockTransport(handler))
    else:
        http = httpx.Client(
            transport=httpx.MockTransport(lambda r: httpx.Response(200, json=QUESTION))
        )
    ticks = iter(now or [1.0, 5.0])
    client = NvimDrillClient(
        "http://test",
        "anon",
        shell=shell,
        http=http,
        now=lambda: next(ticks),
    )
    host = NvimHost(client=client, send=send)
    return host, effects


def test_dispatch_next_emits_question_and_meta():
    host, effects = _make_host()
    host.dispatch({"cmd": "next"})
    types = [e["effect"] for e in effects]
    assert "set_buffer" in types
    assert "question" in types
    # The chatty "loaded into the next cell" line is suppressed on success; the
    # buffer contents and winbar carry that information instead.
    assert "status" not in types
    assert "meta" in types
    meta = next(e for e in effects if e["effect"] == "meta")
    assert meta["question_id"] == 7
    assert meta["topic"] == "iteration/sorting"
    assert meta["due_count"] == 1
    assert meta["new_count"] == 4


def test_dispatch_next_emits_status_when_none_due():
    host, effects = _make_host(
        handler=lambda r: httpx.Response(404, json={"detail": "nothing due"})
    )
    host.dispatch({"cmd": "next"})
    status = next(e for e in effects if e["effect"] == "status")
    assert "remaining" in status["text"].lower()


def test_dispatch_meta_null_when_no_question():
    host, effects = _make_host(
        handler=lambda r: httpx.Response(404, json={"detail": "nothing due"})
    )
    host.dispatch({"cmd": "next"})
    meta = next(e for e in effects if e["effect"] == "meta")
    assert meta["question_id"] is None


# --- NvimHost dispatch: goto -------------------------------------------


def test_dispatch_goto_emits_question_and_meta():
    host, effects = _make_host()
    host.dispatch({"cmd": "goto", "identifier": "7"})
    types = [e["effect"] for e in effects]
    assert "question" in types
    assert "meta" in types
    meta = next(e for e in effects if e["effect"] == "meta")
    assert meta["question_id"] == 7


def test_dispatch_goto_missing_identifier_emits_usage_status():
    host, effects = _make_host()
    host.dispatch({"cmd": "goto", "identifier": ""})
    status = next(e for e in effects if e["effect"] == "status")
    assert "Usage" in status["text"]


def test_dispatch_goto_404_emits_status_and_leaves_no_state():
    host, effects = _make_host(
        handler=lambda r: httpx.Response(404, json={"detail": "no question matches"})
    )
    host.dispatch({"cmd": "goto", "identifier": "999"})
    status = next(e for e in effects if e["effect"] == "status")
    assert "999" in status["text"]
    assert host.client.state is None


def test_dispatch_goto_then_comment_targets_gotod_question():
    def handler(r):
        if r.url.path == "/goto":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(200, json={"event_id": 1})

    host, effects = _make_host(handler=handler)
    host.dispatch({"cmd": "goto", "identifier": "7"})
    effects.clear()
    host.dispatch({"cmd": "comment", "text": "flag this"})
    status = next(e for e in effects if e["effect"] == "status")
    assert "logged" in status["text"].lower()


def test_dispatch_test_emits_tests_effect():
    host, effects = _make_host()
    host.dispatch({"cmd": "next"})
    effects.clear()
    host.dispatch({"cmd": "test", "source": "def solve(lst):\n    return sorted(lst)"})
    types = [e["effect"] for e in effects]
    assert "tests" in types
    tests_eff = next(e for e in effects if e["effect"] == "tests")
    assert tests_eff["passed"] == 2


def test_dispatch_submit_emits_verdict_and_meta():
    def handler(r):
        if r.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(
            200,
            json={
                "verdict": "pass",
                "question_id": 7,
                "hint": None,
                "hint_index": None,
                "judge_comment": "nice",
            },
        )

    host, effects = _make_host(handler=handler, now=[1.0, 5.0, 6.0, 7.0])
    host.dispatch({"cmd": "next"})
    effects.clear()
    host.dispatch({"cmd": "submit", "source": "def solve(lst):\n    return sorted(lst)"})
    types = [e["effect"] for e in effects]
    assert "verdict" in types
    assert "meta" in types


def test_dispatch_begin_restamps_clock_for_latency():
    captured = {}

    def handler(r):
        if r.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        if r.url.path == "/submit":
            captured["latency_ms"] = json.loads(r.content)["latency_ms"]
            return httpx.Response(
                200,
                json={
                    "verdict": "pass",
                    "question_id": 7,
                    "hint": None,
                    "hint_index": None,
                    "judge_comment": "ok",
                },
            )
        return httpx.Response(404)

    # ticks: next fetch_t=1.0, begin=4.0, submit=10.0  → latency = 10.0-4.0 = 6s
    host, effects = _make_host(handler=handler, now=[1.0, 4.0, 10.0])
    host.dispatch({"cmd": "next"})
    host.dispatch({"cmd": "begin"})
    host.dispatch({"cmd": "submit", "source": "def solve(lst):\n    return sorted(lst)"})
    assert captured["latency_ms"] == 6000  # measured from begin, not the 1.0 fetch


def test_dispatch_begin_no_question_is_silent_noop():
    host, effects = _make_host(now=[1.0])
    host.dispatch({"cmd": "begin"})
    assert effects == []  # no effect emitted, no error


def test_dispatch_hint_emits_hint_and_meta():
    def handler(r):
        if r.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(200, json={"hint": "use sorted()", "hint_index": 0, "hints_total": 2})

    host, effects = _make_host(handler=handler)
    host.dispatch({"cmd": "next"})
    effects.clear()
    host.dispatch({"cmd": "hint"})
    types = [e["effect"] for e in effects]
    assert "hint" in types
    assert "meta" in types


def test_dispatch_comment_logs_on_current_question():
    seen = {}

    def handler(r):
        if r.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        if r.url.path == "/question/7/comment" and r.method == "POST":
            seen["path"] = r.url.path
            return httpx.Response(200, json={"event_id": 1})
        return httpx.Response(404)

    host, effects = _make_host(handler=handler)
    host.dispatch({"cmd": "next"})
    effects.clear()
    host.dispatch({"cmd": "comment", "text": "revisit this one"})
    assert seen.get("path") == "/question/7/comment"
    assert any(e["effect"] == "status" and "logged" in e["text"].lower() for e in effects)


def test_dispatch_comment_no_active_question():
    host, effects = _make_host()
    host.dispatch({"cmd": "comment", "text": "x"})
    assert any(e["effect"] == "status" and "no active" in e["text"].lower() for e in effects)


def test_dispatch_comment_empty_text_is_noop():
    posted = {"n": 0}

    def handler(r):
        if r.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        posted["n"] += 1  # any comment POST would bump this
        return httpx.Response(200, json={"event_id": 1})

    host, effects = _make_host(handler=handler)
    host.dispatch({"cmd": "next"})
    effects.clear()
    host.dispatch({"cmd": "comment", "text": "   "})
    assert posted["n"] == 0  # nothing posted
    assert any(
        e["effect"] == "status" and ("empty" in e["text"].lower() or "cancel" in e["text"].lower())
        for e in effects
    )


def test_dispatch_deactivate_current_question():
    seen = {}

    def handler(r):
        if r.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        if r.url.path == "/question/7/active" and r.method == "PATCH":
            seen["patch"] = True
            return httpx.Response(200, json={"question_id": 7, "active": False})
        return httpx.Response(404)

    host, effects = _make_host(handler=handler)
    host.dispatch({"cmd": "next"})
    effects.clear()
    host.dispatch({"cmd": "deactivate"})
    assert seen.get("patch")
    assert any(e["effect"] == "status" and "deactivated" in e["text"].lower() for e in effects)


def test_dispatch_deactivate_no_active_question():
    host, effects = _make_host()
    host.dispatch({"cmd": "deactivate"})
    assert any(e["effect"] == "status" and "no active" in e["text"].lower() for e in effects)


def test_dispatch_bury_emits_status_meta_and_clears_state():
    client, effects = _make_client()  # default handler returns 200 for all paths
    client.do_next()
    effects.clear()
    host = NvimHost(client=client, send=effects.append)
    host.dispatch({"cmd": "bury"})
    assert client.state is None
    assert [e["effect"] for e in effects] == ["status", "meta"]


def test_dispatch_soon_without_active_question_warns():
    client, effects = _make_client()
    host = NvimHost(client=client, send=effects.append)
    host.dispatch({"cmd": "soon"})
    assert effects == [{"effect": "status", "text": "No active question to soon."}]


def test_dispatch_unknown_command():
    host, effects = _make_host()
    host.dispatch({"cmd": "explode"})
    assert any(e["effect"] == "status" and "unknown" in e["text"] for e in effects)


def test_host_corpus_sets_selection():
    host, effects = _make_host()
    host.dispatch({"cmd": "corpus", "name": "pandas"})
    assert host.client.corpus == "pandas"
    assert effects[-1]["effect"] == "status"


# --- NvimHost dispatch: stats ----------------------------------------------

_SESSION_STATS = {
    "session_key": "a1b2c3d4e5f6",
    "questions": 7,
    "pass_count": 5,
    "pass_hinted": 1,
    "fail": 1,
    "avg_latency_ms": 4000,
    "median_latency_ms": 3000,
    "hints_used": 2,
    "cheats": 0,
}

_TOPIC_STATS = [
    {
        "topic": "types/dict",
        "attempts": 12,
        "pass_rate": 0.83,
        "clean_pass_rate": 0.58,
        "avg_latency_ms": 4000,
    },
]


def test_dispatch_stats_session_emits_stats_effect():
    host, effects = _make_host(handler=lambda r: httpx.Response(200, json=_SESSION_STATS))
    host.dispatch({"cmd": "stats", "view": "session"})
    stats = next(e for e in effects if e["effect"] == "stats")
    assert stats["view"] == "session"
    assert "7 questions" in stats["text"]


def test_dispatch_stats_defaults_to_session():
    host, effects = _make_host(handler=lambda r: httpx.Response(200, json=_SESSION_STATS))
    host.dispatch({"cmd": "stats"})
    stats = next(e for e in effects if e["effect"] == "stats")
    assert stats["view"] == "session"


def test_dispatch_stats_passes_filters():
    seen = {}

    def handler(r):
        seen["path"] = r.url.path
        seen["query"] = str(r.url.query)
        return httpx.Response(200, json=_TOPIC_STATS)

    host, effects = _make_host(handler=handler)
    host.dispatch({"cmd": "stats", "view": "topics", "date_range": "7days"})
    assert seen["path"] == "/statistics/topics"
    assert "date_range=7days" in seen["query"]
    assert any(e["effect"] == "stats" for e in effects)


def test_dispatch_stats_unknown_view():
    host, effects = _make_host()
    host.dispatch({"cmd": "stats", "view": "bogus"})
    stats = next(e for e in effects if e["effect"] == "stats")
    assert "Unknown stats view" in stats["text"]


def test_run_processes_multiple_commands():
    host, effects = _make_host()
    lines = [
        '{"cmd": "next"}\n',
        '{"cmd": "test", "source": "def solve(lst): return sorted(lst)"}\n',
    ]
    host.run(inp=lines)
    types = [e["effect"] for e in effects]
    assert "set_buffer" in types
    assert "tests" in types


def test_run_invalid_json_emits_status_error():
    host, effects = _make_host()
    host.run(inp=["not-json\n"])
    assert any(e["effect"] == "status" and "error" in e["text"].lower() for e in effects)


# --- logging hygiene -----------------------------------------------------------

import logging

from drill.client.nvim_host import _quiet_http_logging


def test_quiet_http_logging_suppresses_httpx_info():
    """Even when the ambient environment enables INFO globally, the sidecar
    must not let httpx's 'HTTP Request: ...' line escape to the UI."""
    root = logging.getLogger()
    httpx_logger = logging.getLogger("httpx")
    httpcore_logger = logging.getLogger("httpcore")
    prev_root, prev_httpx, prev_httpcore = (
        root.level,
        httpx_logger.level,
        httpcore_logger.level,
    )
    try:
        root.setLevel(logging.INFO)
        httpx_logger.setLevel(logging.NOTSET)
        httpcore_logger.setLevel(logging.NOTSET)
        assert httpx_logger.isEnabledFor(logging.INFO)  # would spam before the fix

        _quiet_http_logging()

        assert not httpx_logger.isEnabledFor(logging.INFO)
        assert not httpcore_logger.isEnabledFor(logging.INFO)
    finally:
        root.setLevel(prev_root)
        httpx_logger.setLevel(prev_httpx)
        httpcore_logger.setLevel(prev_httpcore)
