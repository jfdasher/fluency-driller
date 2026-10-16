---
kind: idiom
status: approved
topic: types/dict
entry_point: first_occurrence_index
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a value-to-index lookup map from a list
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of strings that may contain duplicates, build a dictionary mapping each unique string to the index of its FIRST occurrence in the list.

## Hints
1. Iterate with enumerate() and only record a value the first time you see it.
2. Check 'if v not in result' before inserting, so duplicates don't overwrite earlier indices.
3. Build an empty dict, loop with enumerate, and add each item only when it's not already a key.
