---
kind: recall
status: approved
topic: types/list
entry_point: drop_last
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
Using slicing, return a new list with the last element removed. Do not use .pop() or del.

## Hints
1. Slicing syntax is lst[start:stop]; negative indices count from the end.
2. To exclude the last element, use -1 as the stop index.
3. Return lst[:-1] to get everything except the last element.
