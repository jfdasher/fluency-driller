---
kind: idiom
status: approved
topic: types/list
entry_point: add_as_element
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
Given a base list `[1, 2, 3]` and an extra list `[4, 5]`, write a function `add_as_element(base, extra)` that returns a NEW list equal to `base` with `extra` appended as a single nested element (do NOT mutate `base`).

## Hints
1. Think about what `list.append` does versus `list.extend` when given a list argument.
2. Use `.copy()` first so the original `base` is not mutated, then call `.append(extra)` on the copy.
3. `.append(extra)` adds `extra` as one item, making it a nested list; `.extend(extra)` would add each item individually.
