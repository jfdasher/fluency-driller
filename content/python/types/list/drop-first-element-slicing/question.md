---
kind: recall
status: approved
topic: types/list
entry_point: drop_first
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: drop the first or last element with slicing
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Using slicing, return a new list with the first element removed. Do not use .pop() or del.

## Hints
1. Slicing syntax is lst[start:stop].
2. To skip the first element, start the slice at index 1.
3. Return lst[1:] to get everything after the first element.
