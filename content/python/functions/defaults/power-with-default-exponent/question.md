---
kind: recall
status: approved
topic: functions/defaults
entry_point: power
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: define a function with a default parameter and call it both with and
    without that argument
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Define a function `power(base, exp=2)` that returns `base` raised to the power `exp`. When called with only one argument, it should square the base by default.

## Hints
1. Give `exp` a default value of `2` in the function signature.
2. Use the `**` operator to raise `base` to the power `exp`.
3. Return `base ** exp`; when called as `power(5)`, Python uses `exp=2` automatically.
