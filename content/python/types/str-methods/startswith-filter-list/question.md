---
kind: idiom
status: approved
topic: types/str-methods
entry_point: filter_by_prefix
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: filter names by prefix with str.startswith
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `filter_by_prefix(names, prefix)` that takes a list of strings and a prefix string, and returns a new list containing only the strings that start with that prefix.

## Hints
1. Iterate over the list and check each element.
2. Use `str.startswith(prefix)` to test each string.
3. A list comprehension with `if name.startswith(prefix)` as the condition is the idiomatic solution.
