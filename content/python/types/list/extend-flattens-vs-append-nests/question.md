---
kind: idiom
status: approved
topic: types/list
entry_point: add_flat
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: extend a list with another vs append it as one element
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `add_flat(base, extra)` that returns a NEW list containing all elements of `base` followed by all individual elements of `extra` (i.e., NOT nested). Do NOT mutate `base`.

## Hints
1. There are two common ways to combine lists: one nests the second list, the other merges its items individually.
2. Use `.copy()` to avoid mutating `base`, then call `.extend(extra)` to add each element of `extra` separately.
3. `.extend(extra)` iterates over `extra` and appends each item one by one, unlike `.append(extra)` which would add the whole list as a single element.
