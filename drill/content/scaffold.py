"""The editor-cell template prefilled for a question.

Single source of truth shared by both clients (to prefill the answer buffer)
and the server (to measure how many characters were prefilled vs authored).
Keep this pure: string in, string out.
"""

from __future__ import annotations


def scaffold(prompt: str, stub: str | None, entry_point: str) -> str:
    comments = "\n".join(f"# {line}" for line in prompt.splitlines())
    body = stub or f"def {entry_point}(...):\n    ..."
    return f"{comments}\n{body}"
