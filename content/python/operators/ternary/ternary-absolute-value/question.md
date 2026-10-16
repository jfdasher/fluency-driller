---
kind: recall
status: approved
topic: operators/ternary
entry_point: absolute_value
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: pick a value with a conditional expression
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Implement `absolute_value(n)` that returns the absolute value of `n` using a single conditional (ternary) expression — do NOT use `abs()` or `if/else` statements.

## Hints
1. A conditional expression has the form: value_if_true if condition else value_if_false.
2. If n is non-negative, return n; otherwise return its negation.
3. return n if n >= 0 else -n
