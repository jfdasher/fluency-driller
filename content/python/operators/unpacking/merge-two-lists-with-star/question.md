---
kind: idiom
status: approved
topic: operators/unpacking
entry_point: merge_lists
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: merge lists or dicts inside a literal with * / **
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `merge_lists(a, b)` that returns a new list containing all elements of `a` followed by all elements of `b`, using the `*` unpacking operator inside a list literal (do NOT use `+` or `.extend`).

## Hints
1. You can unpack iterables inside a list literal with `*`.
2. Try `[*a, *b]` — the `*` spreads each iterable's elements into the new list.
3. The answer is literally `return [*a, *b]`.
