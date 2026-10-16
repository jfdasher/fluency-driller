---
kind: idiom
status: approved
topic: transform-compute/where-mask-select
entry_point: clamp_negatives
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: replace values that fail a condition using Series.where
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a Series `s` of integers, return a new Series where every negative value is replaced with `0`, leaving non-negative values unchanged. Use `Series.where`.

    s
    -------
  0    3
  1   -1
  2    7
  3   -4
  4    0

## Hints
1. Think about what condition should be TRUE for values you want to KEEP.
2. `Series.where(cond, other=...)` keeps values where `cond` is True and replaces them with `other` where it is False.
3. Use `s.where(s >= 0, other=0)` — values satisfying `s >= 0` are kept; all others become 0.
