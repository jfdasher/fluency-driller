---
kind: recall
status: approved
topic: iteration/builtins
entry_point: countdown
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: step through a range with a stride using 3-arg range
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Return a list that counts down from `start` to `stop` (inclusive) in steps of `step` (a positive integer), using a 3-argument `range`. The list should be in descending order.

## Hints
1. A negative step in `range` moves downward; negate the positive `step` argument.
2. `range(start, stop - 1, -step)` includes `stop` by making the exclusive bound one less.
3. Call `list(range(start, stop - 1, -step))` to collect all values from `start` down to `stop`.
