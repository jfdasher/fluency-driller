---
kind: idiom
status: approved
topic: operators/comparison
entry_point: in_inclusive_range
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: test a range with a chained comparison (a < x < b)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `in_inclusive_range(x, lo, hi)` that returns `True` if `x` is between `lo` and `hi` inclusive on both ends, using a single chained comparison expression.

## Hints
1. Python supports chaining comparison operators, so you can combine two checks in one expression.
2. Use `<=` on both sides to include the boundary values.
3. The expression `lo <= x <= hi` evaluates both conditions at once and returns a boolean.
