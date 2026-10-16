"""Single source of truth for running assert-based question tests.

A test is a `def test_*()` function that raises on failure. The runner is kept
as a source snippet (`RUNNER_SRC`) prepended verbatim into the two `python -c`
subprocess drivers (verify, nvim) — which cannot import this package — and also
exec'd here for in-process use by the IPython client. One definition everywhere.

Each test runs in a globals built from the submission's namespace plus injected
`fn` (the entry point) and `equal` (tuple/list-tolerant comparison, retained
from the retired equality module). Failure detail carries only strings, so the
drivers' terminal json.dumps cannot crash on a non-serializable value.
"""

from __future__ import annotations

RUNNER_SRC = r'''
import json as _json
import traceback as _traceback


def _normalize(value):
    """Round-trip through JSON so tuples compare equal to JSON-list values."""
    try:
        return _json.loads(_json.dumps(value))
    except (TypeError, ValueError):
        return value


def equal(got, expected):
    return _normalize(got) == _normalize(expected)


def run_tests(ns, entry_point, tests):
    """Run assert-based test sources against a prepared namespace `ns`.

    ns: namespace already containing the submission's definitions.
    entry_point: name of the function under test (exposed to tests as `fn`).
    tests: list of {"name": str, "source": str}; each source defines `def test_*()`.
    Returns {"passed": int, "failed": int, "detail": [{"name", "reason"}]}.
    """
    passed = 0
    failed = 0
    detail = []
    for t in tests:
        g = dict(ns)
        g["fn"] = ns.get(entry_point)
        g["equal"] = equal
        before = set(g)
        try:
            exec(t["source"], g)
        except Exception as e:
            failed += 1
            detail.append({"name": t.get("name", "?"),
                           "reason": "load error: %s: %s" % (type(e).__name__, e)})
            continue
        test_fns = [(k, g[k]) for k in g
                    if k not in before and k.startswith("test") and callable(g[k])]
        if not test_fns:
            failed += 1
            detail.append({"name": t.get("name", "?"),
                           "reason": "no test function defined"})
            continue
        for name, f in test_fns:
            try:
                f()
                passed += 1
            except Exception as e:
                failed += 1
                tb = _traceback.extract_tb(e.__traceback__)
                reason = "%s: %s" % (type(e).__name__, e)
                if tb and not tb[-1].name.startswith("test"):
                    reason += " (line %d)" % tb[-1].lineno
                detail.append({"name": name, "reason": reason})
    return {"passed": passed, "failed": failed, "detail": detail}
'''

_ns: dict = {}
exec(RUNNER_SRC, _ns)

_normalize = _ns["_normalize"]
equal = _ns["equal"]
run_tests = _ns["run_tests"]
