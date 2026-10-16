---
kind: recall
status: approved
topic: types/list
entry_point: make_zeros
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
Write a function that takes an integer `n` and returns a list of exactly `n` zeros using list multiplication.

## Hints
1. A list can be repeated using the `*` operator.
2. Try `[0] * n` to repeat the element `0` exactly `n` times.
3. The expression `[0] * n` creates a new list with `n` zero elements.
