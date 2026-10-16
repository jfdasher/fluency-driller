---
kind: idiom
status: approved
topic: iteration/sorting
entry_point: sort_keys_by_value_ascending
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: sort dict keys by their associated values
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a dictionary mapping strings to integers, return a list of the keys sorted in ascending order by their associated values. If two keys have the same value, sort them alphabetically.

## Hints
1. Use the built-in `sorted()` function with a `key` argument.
2. The key should be a tuple so that ties in value are broken alphabetically: `key=lambda k: (d[k], k)`.
3. Pass the dictionary directly to `sorted()` — iterating over a dict yields its keys.
