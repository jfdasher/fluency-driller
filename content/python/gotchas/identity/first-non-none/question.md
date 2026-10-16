---
kind: idiom
status: approved
topic: gotchas/identity
entry_point: first_non_none
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: test for None with 'is None' rather than '== None'
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of values, return the first value that is not None. If all values are None, return None. Use the idiomatic Python way to test for None (identity, not equality).

## Hints
1. Loop through the list and return the first element that passes a None-check.
2. Avoid `!= None`; Python style uses identity-based checks for None.
3. Use `is not None` to test whether an element is not None, and return it immediately when found.
