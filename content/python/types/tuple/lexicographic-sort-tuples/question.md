---
kind: recall
status: approved
topic: types/tuple
entry_point: lex_sort
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: compare tuples lexicographically
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of tuples, return a new list sorted in lexicographic (ascending) order. Do not modify the original list.

## Hints
1. Python compares tuples element by element, so tuple comparison is already lexicographic.
2. `sorted()` returns a new list and leaves the original unchanged.
3. Call `sorted(tuples)` with no extra arguments — the default comparison handles lexicographic order.
