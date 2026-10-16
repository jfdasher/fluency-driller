---
kind: idiom
status: approved
topic: types/str-methods
entry_point: normalized_equal
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: case-normalize and strip a string before comparing
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `normalized_equal(a, b)` that returns `True` if strings `a` and `b` are equal after stripping leading/trailing whitespace and converting to lowercase, `False` otherwise.

## Hints
1. Use str.strip() to remove surrounding whitespace from each string before comparing.
2. Use str.lower() to convert both strings to the same case before comparing.
3. Chain the methods: a.strip().lower() == b.strip().lower()
