---
kind: idiom
status: approved
topic: types/dict
entry_point: merge_dicts_pipe
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
Given two dicts `a` and `b`, return a new dict that merges them using the `|` operator. Values from `b` should overwrite values from `a` for duplicate keys.

## Hints
1. Python 3.9+ introduced a merge operator for dicts.
2. The `|` operator on two dicts produces a new merged dict.
3. Return `a | b` directly.
