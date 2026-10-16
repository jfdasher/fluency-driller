"""IPython client: the ``%drill`` magic.

Load with ``%load_ext drill.client``; configure via ``DRILL_URL`` and
``DRILL_USER``. Execution happens entirely client-side — the server never runs
user code. The drilling logic lives in :class:`DrillClient` (testable without a
live kernel or server); the magic is a thin wrapper.

Commands:
    %drill next [KEYWORD]   fetch a question (optionally filtering by topic keyword)
    %drill restate          re-inject the current question's prompt+stub as a new cell
    %drill test             run the question's test cases against your function
    %drill submit           submit your function for judgment
    %drill hint             get the next hint
    %drill cheat            reveal the canonical answer
    %drill soon             repeat this card again soon (drill until grasped)
    %drill bury             push this card well out (I've got this for a while)
    %drill skip             discard the current question without logging
    %drill goto ID          jump to a specific question by id or external_id
    %drill help             show all commands, aliases, and keybindings

Aliases: %dn [KW]  %ds  %dt  %dh  %dc  %dso  %dby  %dr  %dsk  %da

Keybindings (empty cell only):
    Ctrl+]   smart advance — next if no active question, submit otherwise
    Alt+N    next
    Alt+S    submit

Bare ``%drill`` (no subcommand) is context-aware: next if no active question,
submit otherwise. Equivalent to ``%da``.
"""

from __future__ import annotations

import inspect
import os
import time
from collections.abc import Callable
from typing import Any

import httpx
from tabulate import tabulate

from .._runner import _normalize, equal, run_tests  # noqa: F401 — _normalize re-exported
from ..content.scaffold import scaffold

DEFAULT_URL = "http://127.0.0.1:8000"


def format_grading(grading: dict[str, Any]) -> list[str]:
    """Render the SRS grading block as indented lines under the verdict."""

    def human(days: float) -> str:
        if days < 1.0:
            return f"~{round(days * 24 * 60)}min"
        return f"~{days:.0f}d"

    state = "surfaced" if grading["surfaced"] else "scheduled"
    cf = grading["counterfactual_days"]
    return [
        f"   grade: {grading['grade']}  ·  {grading['rationale']}",
        f"   next review: {human(grading['next_interval_days'])}  ·  {grading['phase']}, {state}",
        f"      if GOOD {human(cf['GOOD'])} · if EASY {human(cf['EASY'])} · "
        f"if HARD {human(cf['HARD'])}",
    ]


_HELP_TEXT = """\
%drill / %drill next [KW]   fetch next question  (bare %drill is context-aware)
%drill submit               submit current answer for judgment
%drill test                 run local test cases
%drill hint                 get next hint
%drill cheat                reveal canonical answer
%drill soon                 repeat this card again soon (drill until grasped)
%drill bury                 push this card well out (I've got this for a while)
%drill restate              re-inject question prompt into a new cell
%drill skip                 discard current question
%drill goto ID              jump to a question by id or external_id, bypassing the scheduler
%drill deactivate ID [MSG]  mark question inactive (optionally log a comment)
%drill activate ID [MSG]    mark question active again
%drill toggle ID [MSG]      flip active status
%drill comment ID TEXT      log a comment event for a question
%drill corpus [NAME|all]    set the session's active corpus (default: all)
%drill stats [view] [filter]  show statistics (views: day session topics trends cards coverage)
%drill help                 show this help

Aliases:  %dn [KW]  %ds  %dt  %dh  %dc  %dso  %dby  %dr  %dsk  %da  %dstat [view] [filter]

Keybindings (empty cell only):
  Ctrl+]   smart advance — next if no active question, submit otherwise
  Alt+N    next
  Alt+S    submit"""


class DrillClient:
    def __init__(
        self,
        url: str,
        user: str,
        *,
        shell: Any = None,
        http: httpx.Client | None = None,
        now: Callable[[], float] = time.monotonic,
        corpus: str | None = None,
    ):
        self.url = url.rstrip("/")
        self.user = user
        self.shell = shell
        self.http = http or httpx.Client(timeout=10.0)
        self._now = now
        self.state: dict[str, Any] | None = None
        self.corpus = corpus

    # --- next ---------------------------------------------------------------

    def do_next(self, grader: str | None = None, topic_keyword: str | None = None) -> str:
        params = {"user": self.user}
        if grader:
            params["grader"] = grader
        if topic_keyword:
            params["topic_keyword"] = topic_keyword
        if self.corpus:
            params["corpus"] = self.corpus
        r = self.http.get(f"{self.url}/next", params=params)
        if r.status_code == 404:
            self.state = None
            return "No questions remaining. 🎉"
        r.raise_for_status()
        q = r.json()
        self.state = {
            "question_id": q["question_id"],
            "external_id": q.get("external_id"),
            "topic": q["topic"],
            "entry_point": q["entry_point"],
            "test_cases": q["test_cases"],
            "prompt": q["prompt"],
            "stub": q.get("stub"),
            "fetch_t": self._now(),
            "hints_shown": 0,
            "hints_total": q.get("hints_total", 0),
            "due_count": q.get("due_count", 0),
            "new_count": q.get("new_count", 0),
            "test_output": None,
        }
        if self.shell is not None:
            self.shell.set_next_input(self._render_cell(q))
        due, new = q.get("due_count", 0), q.get("new_count", 0)
        avail = f" ({due + new} available: {due} due, {new} new)"
        tag = self._id_tag(q["question_id"], q.get("external_id"))
        return f"Question {tag} [{q['topic']}] loaded into the next cell.{avail}"

    # --- corpus ---------------------------------------------------------------

    def do_corpus(self, name: str | None) -> str:
        if not name or name.lower() == "all":
            self.corpus = None
            return "Corpus: all (mixing every corpus)."
        self.corpus = name
        return f"Corpus: {name}."

    # --- goto -----------------------------------------------------------------

    def do_goto(self, identifier: str) -> str:
        params: dict[str, Any] = {"user": self.user}
        try:
            params["question_id"] = int(identifier)
        except ValueError:
            params["external_id"] = identifier
            if self.corpus:
                params["corpus"] = self.corpus
        r = self.http.get(f"{self.url}/goto", params=params)
        if r.status_code == 404:
            return f"No question matches {identifier!r}."
        if r.status_code == 409:
            detail = r.json().get("detail", f"Ambiguous: {identifier!r} matches multiple corpora.")
            return f"Ambiguous: {detail}. Set a corpus with %drill corpus <name>."
        r.raise_for_status()
        q = r.json()
        self.state = {
            "question_id": q["question_id"],
            "external_id": q.get("external_id"),
            "topic": q["topic"],
            "entry_point": q["entry_point"],
            "test_cases": q["test_cases"],
            "prompt": q["prompt"],
            "stub": q.get("stub"),
            "fetch_t": self._now(),
            "hints_shown": 0,
            "hints_total": q.get("hints_total", 0),
            "due_count": q.get("due_count", 0),
            "new_count": q.get("new_count", 0),
            "test_output": None,
        }
        if self.shell is not None:
            self.shell.set_next_input(self._render_cell(q))
        tag = self._id_tag(q["question_id"], q.get("external_id"))
        return f"Question {tag} [{q['topic']}] loaded into the next cell."

    @staticmethod
    def _id_tag(question_id: int, external_id: str | None) -> str:
        return f"#{question_id} {external_id}" if external_id else f"#{question_id}"

    @staticmethod
    def _render_cell(q: dict[str, Any]) -> str:
        return scaffold(q["prompt"], q.get("stub"), q["entry_point"])

    # --- restate ------------------------------------------------------------

    def do_restate(self) -> str:
        if self.state is None:
            return "No active question. Run %drill next first."
        cell = self._render_cell(
            {
                "prompt": self.state["prompt"],
                "stub": self.state["stub"],
                "entry_point": self.state["entry_point"],
            }
        )
        if self.shell is not None:
            self.shell.set_next_input(cell)
        return f"Question {self.state['question_id']} restated."

    # --- test ---------------------------------------------------------------

    def do_test(self) -> str:
        if self.state is None:
            return "No active question. Run %drill next first."
        ep = self.state["entry_point"]
        ns = self.shell.user_ns
        if ep not in ns or not callable(ns.get(ep)):
            return f"Define {ep}(...) in a cell and run it first."
        out = run_tests(ns, ep, self.state["test_cases"])
        self.state["test_output"] = out
        return f"{out['passed']} passed, {out['failed']} failed."

    @staticmethod
    def _tests_passed(out: dict | None) -> bool:
        """True iff every test ran and passed (the gate for submitting)."""
        return bool(out) and out.get("failed", 1) == 0 and out.get("passed", 0) > 0

    # --- submit -------------------------------------------------------------

    def mark_started(self) -> None:
        """Re-stamp the latency clock to now.

        Called when the user actually begins answering (Neovim: first
        InsertEnter), so reading/comprehension time before the first keystroke
        is excluded from latency. No-op when there is no active question.
        """
        if self.state is not None:
            self.state["fetch_t"] = self._now()

    def _submit_answer(self, answer_text: str, *, latency_ms: int | None = None) -> str:
        """POST /submit with the given source text; returns formatted verdict string.

        ``latency_ms`` lets a gated caller snapshot recall latency *before*
        running tests; when omitted it is computed at POST time as before.
        """
        if latency_ms is None:
            latency_ms = int((self._now() - self.state["fetch_t"]) * 1000)
        r = self.http.post(
            f"{self.url}/submit",
            json={
                "user": self.user,
                "question_id": self.state["question_id"],
                "answer_text": answer_text,
                "test_output": self.state["test_output"],
                "latency_ms": latency_ms,
                "hints_already_shown": self.state["hints_shown"],
            },
        )
        if r.status_code == 503:
            return "Judge unavailable; please retry."
        r.raise_for_status()
        return self._handle_verdict(r.json())

    def do_submit(self) -> str:
        if self.state is None:
            return "No active question. Run %drill next first."
        fn = self._resolve_fn()
        if fn is None:
            ep = self.state["entry_point"]
            return f"Define {ep}(...) in a cell and run it first."
        try:
            answer_text = inspect.getsource(fn)
        except (OSError, TypeError):
            return "Could not read the source of your function. Define it in a cell."
        # Snapshot recall latency before the test run, then gate on the tests.
        latency_ms = int((self._now() - self.state["fetch_t"]) * 1000)
        out = run_tests(self.shell.user_ns, self.state["entry_point"], self.state["test_cases"])
        self.state["test_output"] = out
        if not self._tests_passed(out):
            return (
                f"❌ {out['passed']} passed, {out['failed']} failed — "
                f"not submitted. Fix the tests first (%drill test for details)."
            )
        return self._submit_answer(answer_text, latency_ms=latency_ms)

    def _handle_verdict(self, resp: dict[str, Any]) -> str:
        verdict = resp["verdict"]
        comment = resp.get("judge_comment") or ""
        tag = self._id_tag(resp["question_id"], resp.get("external_id"))
        grading = resp.get("grading")
        suffix = ("\n" + "\n".join(format_grading(grading))) if grading else ""
        if verdict in ("pass", "pass_hinted"):
            self.state = None
            return f"✅ {verdict} {tag} — {comment}{suffix}"
        hint = resp.get("hint")
        if hint is not None:
            self.state["hints_shown"] += 1  # type: ignore[index]
            idx = resp.get("hint_index")
            total = self.state.get("hints_total", 0)
            if idx is not None and total:
                return f"❌ fail {tag} — {hint}  (hint {idx + 1}/{total}){suffix}"
            return f"❌ fail {tag} — hint: {hint}{suffix}"
        # ladder exhausted; canonical answer arrived in the comment
        return f"❌ fail {tag} — {comment}{suffix}"

    # --- soon / bury --------------------------------------------------------

    def _override(self, kind: str) -> str:
        if self.state is None:
            return "No active question. Run %drill next first."
        qid = self.state["question_id"]
        r = self.http.post(
            f"{self.url}/override",
            json={"user": self.user, "question_id": qid, "kind": kind},
        )
        r.raise_for_status()
        self.state = None
        return f"Will repeat #{qid} soon." if kind == "soon" else f"Buried #{qid} for a while."

    def do_soon(self) -> str:
        return self._override("soon")

    def do_bury(self) -> str:
        return self._override("bury")

    # --- skip ---------------------------------------------------------------

    def do_skip(self) -> str:
        self.state = None
        return "Skipped."

    # --- advance ------------------------------------------------------------

    def do_advance(self, topic_keyword: str | None = None) -> str:
        if self.state is None:
            return self.do_next(topic_keyword=topic_keyword)
        return self.do_submit()

    # --- hint ---------------------------------------------------------------

    def do_hint(self) -> str:
        if self.state is None:
            return "No active question. Run %drill next first."
        r = self.http.get(f"{self.url}/hint", params={"user": self.user})
        if r.status_code == 400:
            return "No active session. Run %drill next first."
        r.raise_for_status()
        resp = r.json()
        hint = resp.get("hint")
        if hint is None:
            return "No more hints. Submit to see the canonical answer."
        idx = resp["hint_index"]
        total = resp["hints_total"]
        self.state["hints_shown"] += 1
        return f"{hint}  (hint {idx + 1}/{total})"

    # --- cheat --------------------------------------------------------------

    def do_cheat(self) -> str:
        if self.state is None:
            return "No active question. Run %drill next first."
        r = self.http.get(f"{self.url}/cheat", params={"user": self.user})
        if r.status_code == 400:
            return "No active session. Run %drill next first."
        r.raise_for_status()
        return r.json()["canonical_answer"]

    # --- stats ------------------------------------------------------------------

    def do_stats(
        self,
        view: str = "session",
        topic_keyword: str | None = None,
        date_range: str | None = None,
    ) -> str:
        if view == "day":
            r = self.http.get(f"{self.url}/statistics/day", params={"user": self.user})
            r.raise_for_status()
            d = r.json()
            latency = f"{d['avg_latency_ms'] // 1000}s" if d["avg_latency_ms"] else "—"
            median = f"{d['median_latency_ms'] // 1000}s" if d["median_latency_ms"] else "—"
            return (
                f"Today {d['date']}  "
                f"{d['questions']} questions  "
                f"pass {d['pass_count']}  hinted {d['pass_hinted']}  fail {d['fail']}  "
                f"avg {latency}  med {median}  hints {d['hints_used']}  cheats {d['cheats']}"
            )

        if view == "session":
            r = self.http.get(f"{self.url}/statistics/session", params={"user": self.user})
            if r.status_code == 400:
                return "No active session. Run %drill next first."
            r.raise_for_status()
            d = r.json()
            latency = f"{d['avg_latency_ms'] // 1000}s" if d["avg_latency_ms"] else "—"
            median = f"{d['median_latency_ms'] // 1000}s" if d["median_latency_ms"] else "—"
            return (
                f"Session {d['session_key'][:8]}…  "
                f"{d['questions']} questions  "
                f"pass {d['pass_count']}  hinted {d['pass_hinted']}  fail {d['fail']}  "
                f"avg {latency}  med {median}  hints {d['hints_used']}  cheats {d['cheats']}"
            )

        if view == "topics":
            params: dict = {"user": self.user}
            if date_range:
                params["date_range"] = date_range
            if self.corpus:
                params["corpus"] = self.corpus
            r = self.http.get(f"{self.url}/statistics/topics", params=params)
            r.raise_for_status()
            rows = r.json()
            if not rows:
                return "No submissions yet."
            table = [
                [
                    row["topic"],
                    row["attempts"],
                    f"{row['pass_rate'] * 100:.0f}%",
                    f"{row['clean_pass_rate'] * 100:.0f}%",
                    f"{row['avg_latency_ms'] // 1000}s" if row["avg_latency_ms"] else "—",
                ]
                for row in rows
            ]
            return tabulate(table, headers=["topic", "attempts", "pass%", "clean%", "avg"])

        if view == "trends":
            params = {"user": self.user}
            if date_range:
                params["date_range"] = date_range
            r = self.http.get(f"{self.url}/statistics/trends", params=params)
            r.raise_for_status()
            rows = r.json()
            if not rows:
                return "No submissions yet."
            table = [
                [
                    row["date"],
                    row["attempts"],
                    f"{row['pass_rate'] * 100:.0f}%",
                    f"{row['avg_latency_ms'] // 1000}s" if row["avg_latency_ms"] else "—",
                ]
                for row in rows
            ]
            return tabulate(table, headers=["date", "attempts", "pass%", "avg"])

        if view == "cards":
            params = {"user": self.user}
            if topic_keyword:
                params["topic"] = topic_keyword
            if date_range:
                params["date_range"] = date_range
            if self.corpus:
                params["corpus"] = self.corpus
            r = self.http.get(f"{self.url}/statistics/cards", params=params)
            r.raise_for_status()
            rows = r.json()
            if not rows:
                return "No cards attempted yet."
            table = [
                [
                    row["external_id"] or str(row["question_id"]),
                    row["attempts"],
                    row["pass_count"],
                    row["last_verdict"] or "—",
                    f"{row['avg_latency_ms'] // 1000}s" if row["avg_latency_ms"] else "—",
                    row["hints_ever"],
                    "Y" if row["cheated"] else "N",
                ]
                for row in rows
            ]
            return tabulate(
                table, headers=["card", "attempts", "pass", "last", "avg", "hints", "cheat"]
            )

        if view == "coverage":
            params = {"user": self.user}
            if self.corpus:
                params["corpus"] = self.corpus
            r = self.http.get(f"{self.url}/statistics/coverage", params=params)
            r.raise_for_status()
            rows = r.json()
            if not rows:
                return "No questions in database."
            table = [
                [
                    row["topic"],
                    row["total_questions"],
                    row["attempted"],
                    f"{row['coverage_pct'] * 100:.0f}%",
                    f"{row['pass_rate'] * 100:.0f}%" if row["pass_rate"] is not None else "—",
                ]
                for row in rows
            ]
            return tabulate(table, headers=["topic", "total", "attempted", "coverage%", "pass%"])

        return f"Unknown stats view '{view}'. Try: session, topics, trends, cards, coverage."

    # --- set_active / comment -----------------------------------------------

    def do_set_active(self, question_id: int, active: bool | None, comment: str | None) -> str:
        body: dict = {} if active is None else {"active": active}
        r = self.http.patch(f"{self.url}/question/{question_id}/active", json=body)
        r.raise_for_status()
        new_active = r.json()["active"]
        state = "activated" if new_active else "deactivated"
        parts = [f"Question {question_id} {state}."]
        if comment:
            cr = self.http.post(
                f"{self.url}/question/{question_id}/comment",
                json={"user": self.user, "comment": comment},
            )
            cr.raise_for_status()
            parts.append("Comment logged.")
        return " ".join(parts)

    def do_comment(self, question_id: int, text: str) -> str:
        r = self.http.post(
            f"{self.url}/question/{question_id}/comment",
            json={"user": self.user, "comment": text},
        )
        r.raise_for_status()
        return f"Comment logged for question {question_id}."

    # --- helpers ------------------------------------------------------------

    def _resolve_fn(self) -> Callable[..., Any] | None:
        if self.shell is None or self.state is None:
            return None
        fn = self.shell.user_ns.get(self.state["entry_point"])
        return fn if callable(fn) else None


# --- IPython integration ----------------------------------------------------


def _register_keybindings(shell: Any) -> None:  # pragma: no cover
    if not (hasattr(shell, "pt_app") and shell.pt_app):
        return
    from prompt_toolkit.application import get_app
    from prompt_toolkit.filters import Condition

    kb = shell.pt_app.key_bindings
    is_empty = Condition(lambda: not get_app().current_buffer.text)

    def _run(event: Any, cmd: str) -> None:
        event.current_buffer.insert_text(cmd)
        event.current_buffer.validate_and_handle()

    # eager=True: prompt_toolkit's Emacs bindings register "c-] + Any" (character
    # search), making c-] a prefix of a two-key sequence. Without eager, the key
    # processor waits the full timeoutlen (1 s) before firing. eager bypasses that.
    @kb.add("c-]", filter=is_empty, eager=True)
    def _advance(event: Any) -> None:
        _run(event, "%da")

    @kb.add("escape", "n", filter=is_empty)
    def _next(event: Any) -> None:
        _run(event, "%dn")

    @kb.add("escape", "s", filter=is_empty)
    def _submit(event: Any) -> None:
        _run(event, "%ds")


def load_ipython_extension(ipython) -> None:  # pragma: no cover
    from IPython.core.magic import Magics, line_magic, magics_class

    client = DrillClient(
        os.environ.get("DRILL_URL", DEFAULT_URL),
        os.environ.get("DRILL_USER", "anon"),
        shell=ipython,
        corpus=os.environ.get("DRILL_CORPUS"),
    )

    @magics_class
    class DrillMagics(Magics):
        def __init__(self, shell):
            super().__init__(shell)
            self._client = client

        @line_magic
        def drill(self, line: str):
            args = line.split()
            cmd = args[0] if args else "advance"
            if cmd == "next":
                keyword = args[1] if len(args) > 1 else None
                print(self._client.do_next(topic_keyword=keyword))
            elif cmd in ("advance", "a"):
                keyword = args[1] if len(args) > 1 else None
                print(self._client.do_advance(topic_keyword=keyword))
            elif cmd == "test":
                print(self._client.do_test())
            elif cmd == "hint":
                print(self._client.do_hint())
            elif cmd == "cheat":
                print(self._client.do_cheat())
            elif cmd == "submit":
                print(self._client.do_submit())
            elif cmd == "skip":
                print(self._client.do_skip())
            elif cmd == "restate":
                print(self._client.do_restate())
            elif cmd == "stats":
                view = args[1] if len(args) > 1 else "session"
                date_range = None
                topic_keyword = None
                for arg in args[2:]:
                    if arg in ("today", "7days", "30days", "all"):
                        date_range = arg
                    else:
                        topic_keyword = arg
                print(
                    self._client.do_stats(view, topic_keyword=topic_keyword, date_range=date_range)
                )
            elif cmd in ("deactivate", "activate", "toggle"):
                if len(args) < 2:
                    print(f"Usage: %drill {cmd} <question_id> [comment]")
                    return
                qid = int(args[1])
                comment = " ".join(args[2:]) if len(args) > 2 else None
                active_val = True if cmd == "activate" else (False if cmd == "deactivate" else None)
                print(self._client.do_set_active(qid, active_val, comment))
            elif cmd == "comment":
                if len(args) < 3:
                    print("Usage: %drill comment <question_id> <text>")
                    return
                qid = int(args[1])
                text = " ".join(args[2:])
                print(self._client.do_comment(qid, text))
            elif cmd == "soon":
                print(self._client.do_soon())
            elif cmd == "bury":
                print(self._client.do_bury())
            elif cmd == "goto":
                if len(args) < 2:
                    print("Usage: %drill goto <question_id_or_external_id>")
                    return
                print(self._client.do_goto(args[1]))
            elif cmd == "corpus":
                name = args[1] if len(args) > 1 else None
                print(self._client.do_corpus(name))
            elif cmd in ("help", "h"):
                print(_HELP_TEXT)
            else:
                print(_HELP_TEXT)

        @line_magic
        def dn(self, line: str):
            keyword = line.strip() or None
            print(self._client.do_next(topic_keyword=keyword))

        @line_magic
        def ds(self, _line: str):
            print(self._client.do_submit())

        @line_magic
        def dt(self, _line: str):
            print(self._client.do_test())

        @line_magic
        def dh(self, _line: str):
            print(self._client.do_hint())

        @line_magic
        def dc(self, _line: str):
            print(self._client.do_cheat())

        @line_magic
        def dso(self, _line: str):
            print(self._client.do_soon())

        @line_magic
        def dby(self, _line: str):
            print(self._client.do_bury())

        @line_magic
        def dr(self, _line: str):
            print(self._client.do_restate())

        @line_magic
        def dsk(self, _line: str):
            print(self._client.do_skip())

        @line_magic
        def da(self, line: str):
            keyword = line.strip() or None
            print(self._client.do_advance(topic_keyword=keyword))

        @line_magic
        def dstat(self, line: str):
            args = line.split()
            view = args[0] if args else "session"
            date_range = None
            topic_keyword = None
            for arg in args[1:]:
                if arg in ("today", "7days", "30days", "all"):
                    date_range = arg
                else:
                    topic_keyword = arg
            print(self._client.do_stats(view, topic_keyword=topic_keyword, date_range=date_range))

    ipython.register_magics(DrillMagics)
    _register_keybindings(ipython)
