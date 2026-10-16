---
kind: idiom
status: approved
topic: iteration/sorting
entry_point: sort_people_by_age_then_name
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: double sort with a lambda as the key
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of (name, age) tuples, return a new list sorted first by age (ascending), then by name (ascending) for people of the same age.

## Hints
1. Use `sorted()` with a `key` argument that extracts information from each tuple.
2. Return a tuple from the lambda to create a composite sort key: primary sort first, tiebreaker second.
3. Use `key=lambda p: (p[1], p[0])` to sort by age (index 1) first, then name (index 0).
