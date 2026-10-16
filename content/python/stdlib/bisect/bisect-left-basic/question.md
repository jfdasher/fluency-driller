---
kind: idiom
status: approved
topic: stdlib/bisect
entry_point: insertion_point
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: find a sorted insertion point with bisect_left
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a sorted list of integers and a target value, return the index at which the target should be inserted to keep the list sorted (leftmost position). Use `bisect.bisect_left`.

## Hints
1. The `bisect` module in the standard library provides tools for working with sorted lists.
2. `bisect.bisect_left(a, x)` returns the leftmost index where `x` can be inserted in sorted list `a`.
3. Call `bisect.bisect_left(sorted_list, target)` directly and return its result.
