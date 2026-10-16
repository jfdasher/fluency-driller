---
kind: idiom
status: approved
topic: gotchas/evaluation-order
entry_point: rotate_left
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: rotate three values in one simultaneous tuple assignment
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given three variables a, b, c, rotate their values left in one simultaneous tuple assignment so that a gets b's value, b gets c's value, and c gets a's original value. Return the new (a, b, c).

## Hints
1. Python evaluates the entire right-hand side before any assignment happens.
2. Use a single tuple assignment: a, b, c = ..., ..., ... where each slot uses the *original* values.
3. The one-liner is: a, b, c = b, c, a
