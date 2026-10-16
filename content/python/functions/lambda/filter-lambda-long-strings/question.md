---
kind: recall
status: approved
topic: functions/lambda
entry_point: keep_long
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: keep only matching items with filter and a lambda
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `keep_long(words, min_len)` that takes a list of strings and an integer `min_len`, and returns a list of only those strings whose length is greater than `min_len`, using `filter` and a `lambda`.

## Hints
1. Use `filter()` with a lambda that checks the length of each string.
2. The lambda receives each word and should return `True` if its length exceeds `min_len`.
3. `lambda w: len(w) > min_len` — remember to wrap `filter(...)` in `list()`.
