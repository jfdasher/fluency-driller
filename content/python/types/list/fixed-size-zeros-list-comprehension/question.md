---
kind: recall
status: approved
topic: types/list
entry_point: zeros_comprehension
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a fixed-size list of zeros
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function that takes an integer `n` and returns a list of exactly `n` zeros using a list comprehension.

## Hints
1. A list comprehension has the form `[expr for var in iterable]`.
2. Use `range(n)` as the iterable and `0` as the expression; the loop variable can be `_` since it is unused.
3. The answer is `[0 for _ in range(n)]`.
