---
kind: idiom
status: approved
topic: types/set
entry_point: count_distinct
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
Given a list of strings `words`, return the number of distinct (unique) strings in the list.

## Hints
1. You need to count only unique values — think about what removes duplicates automatically.
2. Converting the list to a `set` removes all duplicate strings, leaving only distinct ones.
3. Use `len(set(words))` to get the number of unique elements.
