---
kind: idiom
status: approved
topic: types/set
entry_point: deduplicate_list
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: deduplicate a list while keeping only distinct elements via a set
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of integers `nums`, return a new list of the distinct elements (no duplicates) in ascending order. Deduplicate with a `set`.

## Hints
1. Think about a built-in Python data structure that automatically discards duplicates.
2. A `set` holds only unique elements — try converting the list to a set.
3. Use `sorted(set(nums))` to drop duplicates and return them in ascending order.
