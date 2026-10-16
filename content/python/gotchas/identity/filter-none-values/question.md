---
kind: idiom
status: approved
topic: gotchas/identity
entry_point: filter_none_values
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
Given a list of values, return a new list containing only the items that are exactly None. Use the idiomatic Python way to test for None (identity, not equality).

## Hints
1. Iterate over the list and keep only items that satisfy a None-check.
2. Avoid using == to compare with None; Python style prefers identity checks.
3. Use `is None` instead of `== None` inside your list comprehension condition.
