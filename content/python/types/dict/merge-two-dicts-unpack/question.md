---
kind: idiom
status: approved
topic: types/dict
entry_point: merge_dicts_unpack
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: merge two dicts with the | operator or {**a, **b}
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two dicts `a` and `b`, return a new dict that merges them using the `{**a, **b}` unpacking syntax. Values from `b` should overwrite values from `a` for duplicate keys.

## Hints
1. You can spread dict contents into a new dict literal using `**`.
2. Place both dicts inside `{}` with `**` before each to unpack them.
3. Return `{**a, **b}` directly.
