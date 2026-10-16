---
kind: idiom
status: approved
topic: stdlib/bisect
entry_point: insort_single
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: keep a list sorted on insert with bisect.insort
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a sorted list of integers and a new integer value, insert the value into the list in sorted order using `bisect.insort` and return the resulting list. Do not sort the list after insertion.

## Hints
1. The `bisect` module provides utilities for working with sorted lists.
2. `bisect.insort(a, x)` inserts `x` into list `a` while keeping it sorted.
3. Call `bisect.insort(sorted_list, value)` then return `sorted_list`.
