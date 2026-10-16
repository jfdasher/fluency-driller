---
kind: recall
status: approved
topic: types/str-methods
entry_point: split_on_first
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: split on the first delimiter only with str.partition
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Implement `split_on_first(s, sep)` that splits the string `s` at the **first** occurrence of `sep` and returns a tuple `(before, after)`. If `sep` is not found, return `(s, '')`. Use `str.partition`.

## Hints
1. str.partition always returns a 3-tuple: (before, sep, after).
2. Unpack the three parts and discard the middle (the separator itself).
3. Use: before, _, after = s.partition(sep), then return (before, after).
