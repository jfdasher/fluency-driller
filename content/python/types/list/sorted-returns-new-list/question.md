---
kind: idiom
status: approved
topic: types/list
entry_point: sorted_copy
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: sort in place with .sort() vs returning a new list with sorted()
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `sorted_copy(lst)` that returns a **new** sorted list in ascending order without modifying the original `lst`. Use the built-in `sorted()` function.

## Hints
1. `sorted()` takes an iterable and returns a brand-new sorted list, leaving the original unchanged.
2. Pass `lst` to `sorted()` and return the result: `return sorted(lst)`.
3. Do NOT call `lst.sort()` — that modifies in place and returns `None`. Use `sorted(lst)` instead.
