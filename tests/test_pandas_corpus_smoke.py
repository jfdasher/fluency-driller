"""Tracer: a real pandas question verifies end-to-end in the sandbox."""

from pathlib import Path

from drill.content.layout import load_question_dir
from drill.content.verify import verify_question

TRACER_DIR = Path(__file__).resolve().parents[1] / (
    "content/pandas/transform-compute/vectorized-ops/add-total-vectorized"
)


def test_tracer_question_verifies():
    q = load_question_dir(TRACER_DIR)
    assert q.grader == "python"
    assert len(q.tests) == 2
    result = verify_question(q)
    assert result.ok, result.failures
    assert result.failures == []
