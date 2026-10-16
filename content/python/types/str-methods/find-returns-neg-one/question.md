---
kind: idiom
status: approved
topic: types/str-methods
entry_point: safe_find
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
Implement `safe_find(text, sub)` that returns the index of the first occurrence of `sub` in `text`, or `-1` if not found. Use `str.find`.

## Hints
1. str.find returns -1 when the substring is absent.
2. Call text.find(sub) directly — no try/except needed.
3. Return text.find(sub).
