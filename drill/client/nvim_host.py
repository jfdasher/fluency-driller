"""Neovim sidecar: NeovimShell adapter, NvimDrillClient, NvimHost, main()."""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import time

from drill._runner import RUNNER_SRC
from drill.client import DrillClient


def _quiet_http_logging() -> None:
    """Silence httpx/httpcore INFO chatter so the sidecar's channels stay clean.

    The sidecar speaks line-delimited JSON on stdout and surfaces stderr via
    ``vim.notify``. httpx logs every request ("HTTP Request: POST .../submit
    ...") at INFO; whenever the ambient environment has INFO logging enabled,
    that line escapes to stderr and spams the Neovim UI. It's expected/harmless
    in the IPython REPL, but a protocol process must control its own log output
    deterministically rather than inherit ambient config.
    """
    for name in ("httpx", "httpcore"):
        logging.getLogger(name).setLevel(logging.WARNING)


_TEST_DRIVER = (
    RUNNER_SRC
    + r"""
import json, sys
p = json.load(sys.stdin)
ns = {}
try:
    exec(p["code"], ns)
except Exception as e:
    print(json.dumps({"passed": 0, "failed": len(p["tests"]),
        "detail": [{"name": "<submission>",
                    "reason": "submission error: %s: %s" % (type(e).__name__, e)}]}))
    sys.exit(0)
print(json.dumps(run_tests(ns, p["entry_point"], p["tests"])))
"""
)


class NeovimShell:
    """Adapter that makes DrillClient's shell seam emit JSON effects."""

    def __init__(self, send):
        self._send = send
        self.user_ns: dict = {}

    def set_next_input(self, text: str) -> None:
        self._send({"effect": "set_buffer", "text": text})


class NvimDrillClient(DrillClient):
    """DrillClient subclass for the Neovim sidecar.

    Replaces in-process do_test with a timeout-guarded subprocess and adds
    do_submit_from_source so Lua can pass the buffer text directly.
    """

    def __init__(
        self,
        url: str,
        user: str,
        *,
        shell: NeovimShell,
        http=None,
        now=time.monotonic,
        python_argv: list[str] | None = None,
        test_timeout: float = 5.0,
    ):
        super().__init__(url, user, shell=shell, http=http, now=now)
        self._python_argv = python_argv or [sys.executable]
        self._test_timeout = test_timeout

    def do_test_from_source(self, source: str) -> dict:
        if self.state is None:
            return {"passed": 0, "failed": 0, "detail": [], "error": "No active question."}
        payload = json.dumps(
            {
                "code": source,
                "entry_point": self.state["entry_point"],
                "tests": self.state["test_cases"],
            }
        )
        try:
            proc = subprocess.run(
                self._python_argv + ["-c", _TEST_DRIVER],
                input=payload,
                capture_output=True,
                text=True,
                timeout=self._test_timeout,
            )
        except subprocess.TimeoutExpired:
            return {"passed": 0, "failed": 0, "detail": [], "error": "timeout"}
        if proc.returncode != 0:
            msg = proc.stderr.strip() or "driver crashed"
            return {"passed": 0, "failed": 0, "detail": [], "error": msg}
        result = json.loads(proc.stdout)
        self.state["test_output"] = result
        return result

    def do_submit_from_source(self, source: str) -> dict:
        """Gated submit: run tests, only POST when all pass.

        Returns exactly one of:
          {"outcome": "no_state", "message": str}
          {"outcome": "tests_failed", "tests": <test result dict>}
          {"outcome": "submitted", "verdict": <verdict str>}
        """
        if self.state is None:
            return {"outcome": "no_state", "message": "No active question. Run :Drill next first."}
        # Snapshot recall latency before the (subprocess) test run.
        latency_ms = int((self._now() - self.state["fetch_t"]) * 1000)
        result = self.do_test_from_source(source)
        if not self._tests_passed(result):
            return {"outcome": "tests_failed", "tests": result}
        verdict = self._submit_answer(source, latency_ms=latency_ms)
        return {"outcome": "submitted", "verdict": verdict}


class NvimHost:
    """JSON dispatch loop: reads commands from a line sequence, emits effects."""

    def __init__(self, client: NvimDrillClient, send):
        self.client = client
        self._send = send

    def _send_meta(self) -> None:
        state = self.client.state
        if state:
            self._send(
                {
                    "effect": "meta",
                    "topic": state.get("topic", ""),
                    "question_id": state["question_id"],
                    "hints_total": state["hints_total"],
                    "hints_shown": state["hints_shown"],
                    "due_count": state.get("due_count", 0),
                    "new_count": state.get("new_count", 0),
                }
            )
        else:
            self._send(
                {
                    "effect": "meta",
                    "topic": None,
                    "question_id": None,
                    "hints_total": 0,
                    "hints_shown": 0,
                    "due_count": 0,
                    "new_count": 0,
                }
            )

    def dispatch(self, cmd: dict) -> None:
        name = cmd.get("cmd")
        try:
            if name == "next":
                msg = self.client.do_next(topic_keyword=cmd.get("keyword"))
                if self.client.state:
                    # On success the buffer and winbar carry the question and
                    # available counts; skip the chatty status notification.
                    self._send({"effect": "question", "prompt": self.client.state["prompt"]})
                else:
                    self._send({"effect": "status", "text": msg})
                self._send_meta()
            elif name == "goto":
                identifier = (cmd.get("identifier") or "").strip()
                if not identifier:
                    self._send(
                        {
                            "effect": "status",
                            "text": "Usage: :Drill goto <question_id_or_external_id>",
                        }
                    )
                else:
                    msg = self.client.do_goto(identifier)
                    if self.client.state:
                        self._send({"effect": "question", "prompt": self.client.state["prompt"]})
                    else:
                        self._send({"effect": "status", "text": msg})
                    self._send_meta()
            elif name == "test":
                result = self.client.do_test_from_source(cmd.get("source", ""))
                self._send({"effect": "tests", **result})
            elif name == "submit":
                outcome = self.client.do_submit_from_source(cmd.get("source", ""))
                kind = outcome["outcome"]
                if kind == "no_state":
                    self._send({"effect": "status", "text": outcome["message"]})
                elif kind == "tests_failed":
                    self._send({"effect": "tests", **outcome["tests"]})
                else:  # submitted
                    self._send({"effect": "verdict", "text": outcome["verdict"]})
                    self._send_meta()
            elif name == "hint":
                msg = self.client.do_hint()
                self._send({"effect": "hint", "text": msg})
                self._send_meta()
            elif name == "cheat":
                msg = self.client.do_cheat()
                self._send({"effect": "hint", "text": msg})
            elif name == "comment":
                state = self.client.state
                text = (cmd.get("text") or "").strip()
                if not state:
                    self._send({"effect": "status", "text": "No active question to comment."})
                elif not text:
                    self._send({"effect": "status", "text": "Comment cancelled (empty)."})
                else:
                    msg = self.client.do_comment(state["question_id"], text)
                    self._send({"effect": "status", "text": msg})
            elif name == "deactivate":
                state = self.client.state
                if not state:
                    self._send({"effect": "status", "text": "No active question to deactivate."})
                else:
                    comment = cmd.get("text") or None
                    msg = self.client.do_set_active(state["question_id"], False, comment)
                    self._send({"effect": "status", "text": msg})
            elif name in ("soon", "bury"):
                state = self.client.state
                if not state:
                    self._send({"effect": "status", "text": f"No active question to {name}."})
                else:
                    msg = self.client.do_soon() if name == "soon" else self.client.do_bury()
                    self._send({"effect": "status", "text": msg})
                    self._send_meta()
            elif name == "begin":
                # First keystroke in the answer buffer: re-stamp the recall
                # clock. Silent — no effect, no winbar change. No-op if no card.
                self.client.mark_started()
            elif name == "skip":
                msg = self.client.do_skip()
                self._send({"effect": "status", "text": msg})
            elif name == "restate":
                msg = self.client.do_restate()
                if self.client.state:
                    self._send({"effect": "question", "prompt": self.client.state["prompt"]})
                self._send({"effect": "status", "text": msg})
            elif name == "stats":
                view = cmd.get("view") or "session"
                msg = self.client.do_stats(
                    view,
                    topic_keyword=cmd.get("topic_keyword"),
                    date_range=cmd.get("date_range"),
                )
                self._send({"effect": "stats", "view": view, "text": msg})
            elif name == "corpus":
                msg = self.client.do_corpus(cmd.get("name"))
                self._send({"effect": "status", "text": msg})
            else:
                self._send({"effect": "status", "text": f"unknown command: {name!r}"})
        except Exception as exc:
            self._send({"effect": "status", "text": f"error: {exc}"})

    def run(self, inp=None) -> None:
        for raw in inp if inp is not None else sys.stdin:
            line = raw.strip()
            if not line:
                continue
            try:
                cmd = json.loads(line)
            except json.JSONDecodeError:
                self._send({"effect": "status", "text": "error: invalid JSON"})
                continue
            self.dispatch(cmd)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Fluency Driller Neovim sidecar")
    parser.add_argument("--url", default=os.environ.get("DRILL_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--user", default=os.environ.get("DRILL_USER", "anon"))
    parser.add_argument(
        "--python", default=None, help="Comma-separated argv for Python (default: uv,run,python)"
    )
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    _quiet_http_logging()

    python_argv = args.python.split(",") if args.python else ["uv", "run", "python"]

    def _send(effect: dict) -> None:
        sys.stdout.write(json.dumps(effect) + "\n")
        sys.stdout.flush()

    shell = NeovimShell(send=_send)
    client = NvimDrillClient(
        args.url,
        args.user,
        shell=shell,
        python_argv=python_argv,
        test_timeout=args.timeout,
    )
    NvimHost(client=client, send=_send).run()


if __name__ == "__main__":
    main()
