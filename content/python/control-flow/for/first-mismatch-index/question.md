---
kind: idiom
status: approved
topic: control-flow/for
entry_point: first_mismatch_index
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: iterate with enumerate instead of range(len(x))
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two lists `a` and `b` of equal length, return the index of the first position where they differ, or -1 if they are identical. Use `enumerate` instead of `range(len(a))`.

## Hints
1. Loop over `a` while also tracking the current index — there is a built-in that provides both without needing `range(len(a))`.
2. `enumerate(a)` gives you `(i, val)` so you can compare `val` with `b[i]` directly inside the loop.
3. Iterate with `for i, val in enumerate(a):`, check `if val != b[i]: return i`, and return `-1` after the loop.
