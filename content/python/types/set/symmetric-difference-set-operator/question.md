---
kind: recall
status: approved
topic: types/set
entry_point: sym_diff
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: compute intersection, union, and difference with set operators
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two lists `a` and `b`, return a **sorted list** of elements that are in exactly one of the two lists (symmetric difference). Use the set `^` operator.

## Hints
1. The symmetric difference contains elements in a or b but not both.
2. Python sets support the ^ operator for symmetric difference directly.
3. Convert both lists to sets, apply ^, then wrap the result in sorted().
