from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Test(BaseModel):
    """One assert-based test file: `source` defines one or more `def test_*()`."""

    __test__ = False  # not a pytest test class

    name: str
    source: str


class ContentQuestion(BaseModel):
    external_id: str
    topic: str
    grader: str = "python"
    modality: str = "code"
    kind: str  # "idiom" | "recall"
    status: str = "draft"  # "draft" | "approved" | "retired" (retired = excluded from manifest, dir kept as a tombstone)
    prompt: str
    stub: str | None = None
    entry_point: str = "solve"
    canonical_answer: str
    hints: list[str] = []
    tests: list[Test] = []
    provenance: dict[str, Any] | None = None

    def to_import_dict(self) -> dict[str, Any]:
        """Project to the drill-import schema (drops pipeline-only fields)."""
        return {
            "external_id": self.external_id,
            "topic": self.topic,
            "grader": self.grader,
            "modality": self.modality,
            "prompt": self.prompt,
            "stub": self.stub,
            "entry_point": self.entry_point,
            "canonical_answer": self.canonical_answer,
            "hints": list(self.hints),
            "test_cases": [{"name": t.name, "source": t.source} for t in self.tests],
        }
