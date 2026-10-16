---
kind: recall
status: approved
topic: iteration/builtins
entry_point: collect_evens
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
Return a list of all even numbers from 0 up to (but not including) `n` using a 3-argument `range` with a stride of 2.

## Hints
1. Use `range` with three arguments: start, stop, and step.
2. A step of 2 starting from 0 naturally produces even numbers.
3. `list(range(0, n, 2))` collects every other integer beginning at 0.
