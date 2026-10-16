---
kind: idiom
status: approved
topic: types/list
entry_point: copy_list
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: copy a list with [:] instead of aliasing it
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list `original`, return a shallow copy of it using slice idiom. The returned list must be a different object (not an alias) but contain the same elements.

## Hints
1. A plain assignment like `copy = original` creates an alias, not a copy.
2. Slice notation can be used to select all elements: `original[start:stop]` — what happens when both are omitted?
3. Use `original[:]` to create a new list with all the same elements.
