---
kind: idiom
status: approved
topic: types/set
entry_point: count_distinct_chars
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: count distinct elements with len(set(...))
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a string `s`, return the number of distinct characters it contains. Use `len(set(...))` in your solution.

## Hints
1. Strings are iterable, so you can pass one directly to `set()`.
2. Converting a string to a set removes duplicate characters automatically.
3. Return `len(set(s))` to count only the unique characters.
