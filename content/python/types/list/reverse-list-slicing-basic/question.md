---
kind: recall
status: approved
topic: types/list
entry_point: reverse_list
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
Using slice notation `[::-1]`, return a new reversed copy of the given list. Do not use `.reverse()` or `reversed()`.

## Hints
1. Slice notation has three parts: start, stop, and step.
2. A negative step value makes slicing go backwards through the list.
3. Use `lst[::-1]` — omit start and stop so the whole list is covered, with step -1.
