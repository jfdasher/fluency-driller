"""IPython client tests — fake shell + httpx MockTransport, no live server."""

import json

import httpx

from drill.client import DrillClient


# A real module-level def so inspect.getsource can read it back on submit.
def solve(d):
    items = sorted(d.items(), key=lambda kv: kv[0], reverse=True)
    return [list(kv) for kv in sorted(items, key=lambda kv: int(kv[1]))]


def solve_tuples(d):
    # correct answer but as tuples, not lists — exercises normalization
    items = sorted(d.items(), key=lambda kv: kv[0], reverse=True)
    return tuple(tuple(kv) for kv in sorted(items, key=lambda kv: int(kv[1])))


class FakeShell:
    def __init__(self, ns=None):
        self.user_ns = ns if ns is not None else {}
        self.next_input = None

    def set_next_input(self, text):
        self.next_input = text


QUESTION = {
    "question_id": 1,
    "external_id": "sorting/multi-key-stable-mixed",
    "topic": "sorting/multi-key-stable",
    "grader": "python",
    "modality": "code",
    "prompt": "Sort it two ways.",
    "stub": "def solve(d):\n    ...",
    "entry_point": "solve",
    "hints_total": 3,
    "due_count": 3,
    "new_count": 2,
    "test_cases": [
        {
            "name": "test_a",
            "source": (
                "def test_a():\n"
                "    assert equal(fn({'a': '2', 'b': '1', 'c': '2'}), "
                "[['b', '1'], ['c', '2'], ['a', '2']])"
            ),
        },
        {
            "name": "test_b",
            "source": "def test_b():\n    assert equal(fn({'x': '1'}), [['x', '1']])",
        },
    ],
}


def _client(handler, shell=None, now=None):
    http = httpx.Client(transport=httpx.MockTransport(handler))
    ticks = iter(now or [100.0, 104.2])
    return DrillClient(
        "http://test",
        "jim",
        shell=shell or FakeShell(),
        http=http,
        now=lambda: next(ticks),
    )


def _next_handler(request):
    return httpx.Response(200, json=QUESTION)


# --- mark_started -----------------------------------------------------------


def test_mark_started_restamps_fetch_t():
    # fetch at 100.0, begin at 109.0 → clock moves to first-keystroke time.
    c = _client(_next_handler, now=[100.0, 109.0])
    c.do_next()
    assert c.state["fetch_t"] == 100.0
    c.mark_started()
    assert c.state["fetch_t"] == 109.0


def test_mark_started_no_state_is_noop():
    def handler(request):
        return httpx.Response(404)

    c = _client(handler, now=[1.0])
    c.do_next()  # 404 → state stays None
    assert c.state is None
    c.mark_started()  # must not raise
    assert c.state is None


# --- %drill next ------------------------------------------------------------


def test_next_injects_cell_and_stores_state():
    shell = FakeShell()
    c = _client(_next_handler, shell=shell)
    c.do_next()
    assert c.state["question_id"] == 1
    assert c.state["entry_point"] == "solve"
    assert "def solve" in shell.next_input
    assert "# Sort it two ways." in shell.next_input  # prompt rendered as comments


def test_next_message_shows_available_count_breakdown():
    c = _client(_next_handler)
    msg = c.do_next()
    # due_count=3, new_count=2 → 5 available, shown as a breakdown
    assert "(5 available: 3 due, 2 new)" in msg


def test_next_stores_available_counts_in_state():
    c = _client(_next_handler)
    c.do_next()
    assert c.state["due_count"] == 3
    assert c.state["new_count"] == 2


def test_next_stores_external_id_in_state():
    c = _client(_next_handler)
    c.do_next()
    assert c.state["external_id"] == "sorting/multi-key-stable-mixed"


def test_next_message_includes_id_tag():
    c = _client(_next_handler)
    msg = c.do_next()
    assert "#1 sorting/multi-key-stable-mixed" in msg


def test_next_404_degrades_gracefully():
    def handler(request):
        return httpx.Response(404, json={"detail": "no questions remaining"})

    c = _client(handler)
    msg = c.do_next()
    assert c.state is None
    assert "no questions" in msg.lower()


# --- %drill test ------------------------------------------------------------


def test_test_runs_cases_and_caches_output():
    shell = FakeShell({"solve": solve})
    c = _client(_next_handler, shell=shell)
    c.do_next()
    c.do_test()
    assert c.state["test_output"] == {"passed": 2, "failed": 0, "detail": []}


def test_test_normalizes_tuples_vs_lists():
    shell = FakeShell({"solve": solve_tuples})
    c = _client(_next_handler, shell=shell)
    c.do_next()
    c.do_test()
    # solve_tuples returns tuples; expected are JSON lists — must still match
    assert c.state["test_output"]["failed"] == 0


def test_test_without_defined_function():
    shell = FakeShell()  # no `solve`
    c = _client(_next_handler, shell=shell)
    c.do_next()
    msg = c.do_test()
    assert "solve" in msg


def test_do_test_runs_assert_tests_against_shell_ns():
    shell = FakeShell({"make": lambda f: lambda x: x * f})
    c = DrillClient("http://x", "u", shell=shell)
    c.state = {
        "entry_point": "make",
        "test_cases": [
            {"name": "test_a", "source": "def test_a():\n    assert make(3)(5) == 15"},
            {"name": "test_b", "source": "def test_b():\n    assert fn(0)(9) == 0"},
        ],
        "test_output": None,
    }
    c.do_test()
    assert c.state["test_output"]["passed"] == 2
    assert c.state["test_output"]["failed"] == 0


def test_do_test_reports_failing_assert_reason():
    shell = FakeShell({"make": lambda f: lambda x: x * f})
    c = DrillClient("http://x", "u", shell=shell)
    c.state = {
        "entry_point": "make",
        "test_cases": [{"name": "test_a", "source": "def test_a():\n    assert make(3)(5) == 999"}],
        "test_output": None,
    }
    c.do_test()
    out = c.state["test_output"]
    assert out["failed"] == 1 and "AssertionError" in out["detail"][0]["reason"]


def test_tests_passed_predicate():
    p = DrillClient._tests_passed
    assert p({"passed": 2, "failed": 0, "detail": []}) is True
    assert p({"passed": 0, "failed": 0, "detail": []}) is False  # nothing ran
    assert p({"passed": 1, "failed": 1, "detail": []}) is False  # a failure
    assert p({"passed": 0, "failed": 0, "error": "timeout"}) is False
    assert p(None) is False
    assert p({}) is False


# --- %drill submit ----------------------------------------------------------


def test_submit_sends_source_latency_and_test_output():
    captured = {}

    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        captured["body"] = _json(request)
        return httpx.Response(
            200,
            json={
                "verdict": "pass",
                "question_id": 1,
                "hint": None,
                "hint_index": None,
                "judge_comment": "nice",
            },
        )

    shell = FakeShell({"solve": solve})
    c = _client(handler, shell=shell, now=[100.0, 105.0])
    c.do_next()
    c.do_test()
    msg = c.do_submit()
    body = captured["body"]
    assert "def solve" in body["answer_text"]
    assert body["test_output"]["passed"] == 2
    assert body["latency_ms"] == 5000
    assert body["hints_already_shown"] == 0
    assert "pass" in msg
    assert c.state is None  # cleared on pass


def test_submit_fail_with_hint_increments_local_counter():
    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(
            200,
            json={
                "verdict": "fail",
                "question_id": 1,
                "hint": "two-pass sort",
                "hint_index": 0,
                "judge_comment": "wrong idiom",
            },
        )

    shell = FakeShell({"solve": solve})
    c = _client(handler, shell=shell, now=[1.0, 2.0])
    c.do_next()
    msg = c.do_submit()
    assert "two-pass sort" in msg
    assert "(hint 1/3)" in msg
    assert c.state["hints_shown"] == 1


def test_submit_503_keeps_state():
    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(503, json={"detail": "judge unavailable; retry"})

    shell = FakeShell({"solve": solve})
    c = _client(handler, shell=shell, now=[1.0, 2.0])
    c.do_next()
    msg = c.do_submit()
    assert "unavailable" in msg.lower() or "retry" in msg.lower()
    assert c.state is not None  # not cleared, can retry


def test_submit_without_active_question():
    c = _client(_next_handler)
    msg = c.do_submit()
    assert "next" in msg.lower()


def test_submit_runs_tests_and_posts_fresh_output():
    captured = {}

    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        captured["body"] = _json(request)
        return httpx.Response(
            200,
            json={
                "verdict": "pass",
                "question_id": 1,
                "hint": None,
                "hint_index": None,
                "judge_comment": "",
            },
        )

    # passing function, but %drill test was never called explicitly
    c = _client(handler, shell=FakeShell({"solve": solve}), now=[1.0, 2.0])
    c.do_next()
    c.do_submit()
    # submit ran the tests itself and sent the fresh all-pass output
    assert captured["body"]["test_output"]["passed"] == 2
    assert captured["body"]["test_output"]["failed"] == 0


def test_submit_blocked_when_tests_fail():
    posted = {"n": 0}

    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        posted["n"] += 1  # any /submit POST bumps this
        return httpx.Response(
            200,
            json={
                "verdict": "pass",
                "question_id": 1,
                "hint": None,
                "hint_index": None,
                "judge_comment": "",
            },
        )

    # a wrong solution: returns the dict's keys, fails QUESTION's asserts
    def bad(d):
        return list(d.keys())

    c = _client(handler, shell=FakeShell({"solve": bad}), now=[1.0, 2.0])
    c.do_next()
    msg = c.do_submit()
    assert posted["n"] == 0  # never POSTed
    assert "failed" in msg.lower()  # reported test failure locally
    assert c.state is not None  # not cleared — still on this question


def test_do_next_stores_topic():
    shell = FakeShell()
    c = _client(_next_handler, shell=shell)
    c.do_next()
    assert c.state["topic"] == "sorting/multi-key-stable"


def test_submit_answer_shared_path():
    """_submit_answer(text) is the same POST path as do_submit."""
    captured = {}

    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        captured["body"] = _json(request)
        return httpx.Response(
            200,
            json={
                "verdict": "pass",
                "question_id": 1,
                "hint": None,
                "hint_index": None,
                "judge_comment": "nice",
            },
        )

    shell = FakeShell({"solve": solve})
    c = _client(handler, shell=shell, now=[100.0, 105.0])
    c.do_next()
    msg = c._submit_answer("def solve(d):\n    return []")
    assert "pass" in msg
    assert "def solve" in captured["body"]["answer_text"]


def test_submit_answer_uses_explicit_latency_override():
    captured = {}

    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        captured["body"] = _json(request)
        return httpx.Response(
            200,
            json={
                "verdict": "pass",
                "question_id": 1,
                "hint": None,
                "hint_index": None,
                "judge_comment": "ok",
            },
        )

    # only one now() tick is consumed (do_next); the override must skip _now()
    c = _client(handler, shell=FakeShell({"solve": solve}), now=[100.0])
    c.do_next()
    c._submit_answer("def solve(d):\n    return []", latency_ms=7777)
    assert captured["body"]["latency_ms"] == 7777


# --- %drill skip ------------------------------------------------------------


def test_skip_clears_state():
    c = _client(_next_handler)
    c.do_next()
    c.do_skip()
    assert c.state is None


import json as _jsonlib


def _json(request: httpx.Request) -> dict:
    return _jsonlib.loads(request.content.decode())


# --- %drill stats / do_stats ------------------------------------------------

STATS_SESSION = {
    "session_key": "abc12345-xxxx",
    "questions": 3,
    "pass_count": 2,
    "pass_hinted": 1,
    "fail": 0,
    "hints_used": 2,
    "cheats": 0,
    "avg_latency_ms": 42000,
    "median_latency_ms": 42000,
}

STATS_TOPICS = [
    {
        "topic": "sorting/multi-key-stable",
        "attempts": 3,
        "pass_count": 2,
        "pass_hinted": 1,
        "fail": 0,
        "pass_rate": 1.0,
        "clean_pass_rate": 0.667,
        "avg_latency_ms": 42000,
    }
]

STATS_COVERAGE = [
    {
        "topic": "sorting/multi-key-stable",
        "total_questions": 5,
        "attempted": 3,
        "coverage_pct": 0.6,
        "pass_rate": 1.0,
    }
]


STATS_DAY = {
    "date": "2026-06-16",
    "questions": 3,
    "pass_count": 2,
    "pass_hinted": 1,
    "fail": 0,
    "hints_used": 2,
    "cheats": 0,
    "avg_latency_ms": 42000,
    "median_latency_ms": 42000,
}


def _stats_handler(request):
    path = str(request.url.path)
    if path == "/statistics/session":
        return httpx.Response(200, json=STATS_SESSION)
    if path == "/statistics/topics":
        return httpx.Response(200, json=STATS_TOPICS)
    if path == "/statistics/trends":
        return httpx.Response(200, json=[])
    if path == "/statistics/cards":
        return httpx.Response(200, json=[])
    if path == "/statistics/coverage":
        return httpx.Response(200, json=STATS_COVERAGE)
    if path == "/statistics/day":
        return httpx.Response(200, json=STATS_DAY)
    return httpx.Response(404)


def test_do_stats_session():
    c = _client(_stats_handler)
    result = c.do_stats("session")
    assert "abc12345" in result
    assert "3" in result  # questions
    assert "avg 42s" in result  # average latency
    assert "med 42s" in result  # median latency


def test_do_stats_topics():
    c = _client(_stats_handler)
    result = c.do_stats("topics")
    assert "sorting/multi-key-stable" in result
    assert "100%" in result  # pass_rate


def test_do_stats_coverage():
    c = _client(_stats_handler)
    result = c.do_stats("coverage")
    assert "sorting/multi-key-stable" in result
    assert "60%" in result  # coverage_pct


def test_do_stats_unknown_view():
    c = _client(_stats_handler)
    result = c.do_stats("bogus")
    assert "bogus" in result


def test_do_stats_day():
    c = _client(_stats_handler)
    result = c.do_stats("day")
    assert "2026-06-16" in result
    assert "3" in result  # questions
    assert "avg 42s" in result  # average latency
    assert "med 42s" in result  # median latency


# --- %drill hint ------------------------------------------------------------


def test_hint_returns_hint_with_position():
    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(200, json={"hint": "Sort twice", "hint_index": 0, "hints_total": 3})

    c = _client(handler)
    c.do_next()
    msg = c.do_hint()
    assert "Sort twice" in msg
    assert "(hint 1/3)" in msg
    assert c.state["hints_shown"] == 1


def test_hint_exhausted_message():
    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(200, json={"hint": None, "hint_index": None, "hints_total": 3})

    c = _client(handler)
    c.do_next()
    msg = c.do_hint()
    assert "no more hints" in msg.lower()
    assert c.state["hints_shown"] == 0  # not incremented when exhausted


def test_hint_without_active_question():
    c = _client(_next_handler)
    msg = c.do_hint()
    assert "next" in msg.lower()


# --- %drill cheat -----------------------------------------------------------


def test_cheat_returns_canonical_answer():
    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(200, json={"canonical_answer": "def solve(d):\n    return 1"})

    c = _client(handler)
    c.do_next()
    msg = c.do_cheat()
    assert "def solve" in msg
    assert c.state is not None  # state not cleared; user may still submit


def test_cheat_without_active_question():
    c = _client(_next_handler)
    msg = c.do_cheat()
    assert "next" in msg.lower()


# --- %drill restate ---------------------------------------------------------


def test_restate_reinjects_cell():
    shell = FakeShell()
    c = _client(_next_handler, shell=shell)
    c.do_next()
    shell.next_input = None  # simulate user overwriting the cell
    msg = c.do_restate()
    assert shell.next_input is not None
    assert "# Sort it two ways." in shell.next_input
    assert "def solve" in shell.next_input
    assert "Question 1" in msg


def test_restate_without_active_question():
    c = _client(_next_handler)
    msg = c.do_restate()
    assert "next" in msg.lower()


# --- topic_keyword filter ---------------------------------------------------


def test_next_sends_topic_keyword():
    """do_next(topic_keyword=...) passes ?topic_keyword= to the server."""
    captured = {}

    def handler(request):
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=QUESTION)

    c = _client(handler)
    c.do_next(topic_keyword="sorting")
    assert captured["params"].get("topic_keyword") == "sorting"


# --- %drill corpus (sticky, client-side) -------------------------------------


def test_corpus_sticky_threads_into_next():
    captured = {}

    def handler(request):
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=QUESTION)

    c = _client(handler)
    c.do_corpus("pandas")
    assert c.corpus == "pandas"
    c.do_next()
    assert captured["params"].get("corpus") == "pandas"


def test_corpus_all_clears():
    captured = {}

    def handler(request):
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=QUESTION)

    c = _client(handler)
    c.do_corpus("pandas")
    msg = c.do_corpus("all")
    assert c.corpus is None
    assert msg
    c.do_next()
    assert "corpus" not in captured["params"]


# --- %drill advance (context-aware next-or-submit) --------------------------


def test_advance_fetches_next_when_no_state():
    shell = FakeShell()
    c = _client(_next_handler, shell=shell)
    msg = c.do_advance()
    assert c.state is not None
    assert "Question #1" in msg


def test_advance_submits_when_state_active():
    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(
            200,
            json={
                "verdict": "pass",
                "question_id": 1,
                "hint": None,
                "hint_index": None,
                "judge_comment": "nice",
            },
        )

    shell = FakeShell({"solve": solve})
    c = _client(handler, shell=shell, now=[100.0, 105.0])
    c.do_next()
    c.do_test()
    msg = c.do_advance()
    assert "pass" in msg
    assert c.state is None  # cleared on pass


def test_advance_forwards_topic_keyword_to_next():
    captured = {}

    def handler(request):
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=QUESTION)

    c = _client(handler)
    c.do_advance(topic_keyword="sorting")
    assert captured["params"].get("topic_keyword") == "sorting"


# --- _HELP_TEXT completeness ------------------------------------------------

from drill.client import _HELP_TEXT


def test_help_text_contains_all_commands_aliases_and_keybindings():
    expected_tokens = [
        # long-form commands
        "%drill next",
        "%drill submit",
        "%drill test",
        "%drill hint",
        "%drill cheat",
        "%drill restate",
        "%drill skip",
        "%drill help",
        # aliases
        "%dn",
        "%ds",
        "%dt",
        "%dh",
        "%dc",
        "%dr",
        "%dsk",
        "%da",
        # keybindings
        "Ctrl+]",
        "Alt+N",
        "Alt+S",
        # new subcommands
        "%drill deactivate",
        "%drill activate",
        "%drill toggle",
        "%drill comment",
        "%drill goto",
    ]
    for token in expected_tokens:
        assert token in _HELP_TEXT, f"Missing from _HELP_TEXT: {token!r}"


# --- %drill deactivate / activate / toggle / comment ------------------------

import json as _jsonmod


def test_do_deactivate():
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(200, json={"question_id": 23, "active": False})

    c = _client(handler)
    msg = c.do_set_active(23, False, None)
    assert "deactivated" in msg
    assert len(calls) == 1
    assert calls[0].method == "PATCH"
    assert _jsonmod.loads(calls[0].content) == {"active": False}


def test_do_activate():
    def handler(request):
        return httpx.Response(200, json={"question_id": 5, "active": True})

    c = _client(handler)
    msg = c.do_set_active(5, True, None)
    assert "activated" in msg


def test_do_toggle():
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(200, json={"question_id": 7, "active": False})

    c = _client(handler)
    msg = c.do_set_active(7, None, None)
    assert "deactivated" in msg
    assert _jsonmod.loads(calls[0].content) == {}


def test_do_set_active_with_comment():
    calls = []

    def handler(request):
        calls.append((request.method, request.url.path))
        if request.method == "PATCH":
            return httpx.Response(200, json={"question_id": 23, "active": False})
        return httpx.Response(200, json={"event_id": 42})

    c = _client(handler)
    msg = c.do_set_active(23, False, "bad question")
    assert "deactivated" in msg
    assert "Comment logged" in msg
    assert ("PATCH", "/question/23/active") in calls
    assert ("POST", "/question/23/comment") in calls


def test_do_comment():
    def handler(request):
        return httpx.Response(200, json={"event_id": 99})

    c = _client(handler)
    msg = c.do_comment(10, "needs rewrite")
    assert "10" in msg
    assert "logged" in msg.lower()


# --- %drill goto --------------------------------------------------------


def test_do_goto_by_question_id():
    captured = {}

    def handler(request):
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=QUESTION)

    c = _client(handler)
    c.do_goto("1")
    assert captured["params"] == {"user": "jim", "question_id": "1"}
    assert c.state["question_id"] == 1
    assert c.state["external_id"] == "sorting/multi-key-stable-mixed"


def test_do_goto_by_external_id():
    captured = {}

    def handler(request):
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=QUESTION)

    c = _client(handler)
    c.do_goto("iteration/sorting/foo")
    assert captured["params"] == {"user": "jim", "external_id": "iteration/sorting/foo"}


def test_do_goto_404_leaves_no_state():
    def handler(request):
        return httpx.Response(404, json={"detail": "no question matches"})

    c = _client(handler)
    msg = c.do_goto("nope")
    assert c.state is None
    assert "nope" in msg


def test_do_goto_threads_sticky_corpus_by_external_id():
    captured = {}

    def handler(request):
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=QUESTION)

    c = _client(handler)
    c.do_corpus("pandas")
    c.do_goto("iteration/sorting/foo")
    assert captured["params"].get("corpus") == "pandas"


def test_do_goto_409_ambiguous_external_id_returns_friendly_message():
    def handler(request):
        return httpx.Response(
            409,
            json={"detail": "external_id 'a/1' exists in corpora: pandas, python"},
        )

    c = _client(handler)
    msg = c.do_goto("a/1")
    assert c.state is None
    assert "pandas" in msg and "python" in msg
    assert "Ambiguous" in msg or "ambiguous" in msg


def test_do_goto_injects_cell():
    shell = FakeShell()
    c = _client(lambda r: httpx.Response(200, json=QUESTION), shell=shell)
    c.do_goto("1")
    assert "def solve" in shell.next_input


# --- id tag on verdict messages ------------------------------------------


def test_verdict_pass_message_includes_id_tag():
    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(
            200,
            json={
                "verdict": "pass",
                "question_id": 1,
                "external_id": "sorting/multi-key-stable-mixed",
                "hint": None,
                "hint_index": None,
                "judge_comment": "nice",
            },
        )

    shell = FakeShell({"solve": solve})
    c = _client(handler, shell=shell)
    c.do_next()
    msg = c.do_submit()
    assert "#1 sorting/multi-key-stable-mixed" in msg


def test_verdict_fail_message_includes_id_tag():
    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        return httpx.Response(
            200,
            json={
                "verdict": "fail",
                "question_id": 1,
                "external_id": "sorting/multi-key-stable-mixed",
                "hint": "two-pass sort",
                "hint_index": 0,
                "judge_comment": "wrong idiom",
            },
        )

    shell = FakeShell({"solve": solve})
    c = _client(handler, shell=shell)
    c.do_next()
    msg = c.do_submit()
    assert "#1 sorting/multi-key-stable-mixed" in msg


# --- %drill soon / %drill bury ----------------------------------------------


def _override_handler(seen):
    def handler(request):
        if request.url.path == "/next":
            return httpx.Response(200, json=QUESTION)
        if request.url.path == "/override":
            seen["body"] = json.loads(request.content)
            return httpx.Response(
                200, json={"question_id": 1, "kind": seen.get("expected", "soon"), "event_id": 9}
            )
        return httpx.Response(404)

    return handler


def test_do_bury_posts_and_clears_state():
    seen = {"expected": "bury"}
    c = _client(_override_handler(seen))
    c.do_next()
    msg = c.do_bury()
    assert seen["body"] == {"user": "jim", "question_id": 1, "kind": "bury"}
    assert c.state is None
    assert "#1" in msg


def test_do_soon_posts_and_clears_state():
    seen = {"expected": "soon"}
    c = _client(_override_handler(seen))
    c.do_next()
    msg = c.do_soon()
    assert seen["body"] == {"user": "jim", "question_id": 1, "kind": "soon"}
    assert c.state is None
    assert "#1" in msg


def test_do_soon_without_active_question():
    c = _client(_override_handler({}))
    assert "No active question" in c.do_soon()


def test_format_grading_lines():
    from drill.client import format_grading

    lines = format_grading(
        {
            "grade": "EASY",
            "rationale": "recall 35.6s vs 22s typing budget (+20s grace), clean, 0 hints",
            "phase": "REVIEW",
            "surfaced": True,
            "next_interval_days": 9.0,
            "next_due": "2026-07-08T12:00:00+00:00",
            "counterfactual_days": {"GOOD": 7.0, "EASY": 9.0, "HARD": 3.0},
        }
    )
    body = "\n".join(lines)
    assert "EASY" in body
    assert "recall 35.6s" in body
    assert "REVIEW" in body
    assert "surfaced" in body
    assert "if GOOD" in body and "if HARD" in body


def test_handle_verdict_includes_grading():
    from drill.client import DrillClient

    c = DrillClient.__new__(DrillClient)
    c.state = {"hints_shown": 0, "hints_total": 0}
    out = c._handle_verdict(
        {
            "verdict": "pass",
            "question_id": 1,
            "external_id": "t/x",
            "judge_comment": "good",
            "grading": {
                "grade": "GOOD",
                "rationale": "recall 3.0s vs 5s typing budget (+20s grace), clean, 0 hints",
                "phase": "REVIEW",
                "surfaced": False,
                "next_interval_days": 4.0,
                "next_due": "2026-07-03T00:00:00+00:00",
                "counterfactual_days": {"GOOD": 4.0, "EASY": 5.0, "HARD": 1.0},
            },
        }
    )
    assert "✅ pass" in out
    assert "grade: GOOD" in out
    assert "next review" in out
