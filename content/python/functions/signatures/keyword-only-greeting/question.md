---
kind: recall
status: approved
topic: functions/signatures
entry_point: greet
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: force a parameter to be keyword-only with a bare *
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Define a function `greet(name, *, greeting)` that returns the string `'{greeting}, {name}!'`. The `greeting` parameter must be keyword-only (enforced by a bare `*`). Do not provide a default for `greeting`.

## Hints
1. A bare `*` in the parameter list marks every parameter after it as keyword-only.
2. Place `*` between `name` and `greeting` so `greeting` cannot be passed positionally.
3. The signature should be `def greet(name, *, greeting):` – the `*` alone (no name) forces keyword-only.
