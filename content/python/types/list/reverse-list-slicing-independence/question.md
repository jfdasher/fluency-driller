---
kind: recall
status: approved
topic: types/list
entry_point: reversed_copy
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: reverse a list with slicing [::-1]
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Using slice notation `[::-1]`, return a new reversed list such that modifying the returned list does NOT affect the original. The function should return the reversed copy.

## Hints
1. Slicing a list always creates a new list object, so the original is unaffected.
2. A step of -1 in a slice iterates from the last element to the first.
3. The expression `lst[::-1]` returns a brand-new reversed list without mutating `lst`.
