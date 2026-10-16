---
kind: idiom
status: approved
topic: functions/closures
entry_point: make_multiplier
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a multiplier factory that returns a closure
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `make_multiplier(factor)` that returns a new function. The returned function should accept a single number `x` and return `x * factor`.

## Hints
1. The outer function should define and return an inner function.
2. The inner function captures `factor` from the enclosing scope — this is a closure.
3. Inside `make_multiplier`, write `def inner(x): return x * factor` and then `return inner`.
