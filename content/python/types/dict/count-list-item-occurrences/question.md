---
kind: idiom
status: approved
topic: types/dict
entry_point: count_items
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: count occurrences with counts.get(key, 0) + 1
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `count_items(items)` that takes a list of hashable items and returns a dictionary mapping each item to the number of times it appears in the list. Use the default fallback idiom (do not use `collections.Counter`).

## Hints
1. Initialize an empty dictionary and iterate over each element in `items`.
2. For each element, look it up with `counts.get(item, 0)` and add 1 before storing it back.
3. The body is just `counts[item] = counts.get(item, 0) + 1` inside the loop; return `counts` at the end.
