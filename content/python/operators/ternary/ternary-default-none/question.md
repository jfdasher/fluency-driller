---
kind: idiom
status: approved
topic: operators/ternary
entry_point: safe_upper
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: place a value-ternary vs a comprehension if-clause correctly
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `safe_upper(s)` that returns `s.upper()` if `s` is not None, otherwise returns the string `'N/A'`. Use a single ternary expression (not if/else statements).

## Hints
1. A ternary expression has the form: value_if_true if condition else value_if_false.
2. Check whether s is None using `s is not None` as the condition.
3. Return `s.upper() if s is not None else 'N/A'` as a single expression.
