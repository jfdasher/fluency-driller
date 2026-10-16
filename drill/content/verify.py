from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field

from .._runner import RUNNER_SRC
from .schema import ContentQuestion

_DRIVER = RUNNER_SRC + r"""
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


@dataclass
class VerifyResult:
    ok: bool
    failures: list[str] = field(default_factory=list)


def verify_question(q: ContentQuestion, timeout: float = 5.0) -> VerifyResult:
    """Run the canonical answer against every test in an isolated subprocess."""
    payload = json.dumps({
        "code": q.canonical_answer,
        "entry_point": q.entry_point,
        "tests": [{"name": t.name, "source": t.source} for t in q.tests],
    })
    try:
        proc = subprocess.run(
            [sys.executable, "-c", _DRIVER],
            input=payload, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return VerifyResult(ok=False, failures=[f"timeout after {timeout}s"])
    if proc.returncode != 0:
        return VerifyResult(ok=False, failures=[f"driver crashed: {proc.stderr.strip()}"])
    data = json.loads(proc.stdout)
    failures = [f"{d['name']}: {d['reason']}" for d in data["detail"]]
    return VerifyResult(ok=data["failed"] == 0, failures=failures)
