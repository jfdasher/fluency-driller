---
kind: idiom
status: approved
topic: gotchas/evaluation-order
entry_point: rotate_right
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
Given three variables a, b, c, rotate their values right in one simultaneous tuple assignment so that a gets c's value, b gets a's original value, and c gets b's original value. Return the new (a, b, c).

## Hints
1. Python evaluates the entire right-hand side before assigning, so no temporary variable is needed.
2. Think about where each original value needs to land: original c -> a, original a -> b, original b -> c.
3. The one-liner is: a, b, c = c, a, b
