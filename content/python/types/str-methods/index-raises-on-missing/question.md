---
kind: idiom
status: approved
topic: types/str-methods
entry_point: strict_find
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: locate a substring with find (returns -1) vs index (raises)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Implement `strict_find(text, sub)` that returns the index of the first occurrence of `sub` in `text`, raising a `ValueError` if not found. Use `str.index`.

## Hints
1. str.index raises ValueError when the substring is absent — unlike find.
2. Call text.index(sub) directly; the exception propagates automatically.
3. Return text.index(sub).
