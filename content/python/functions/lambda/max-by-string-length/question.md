---
kind: idiom
status: approved
topic: functions/lambda
entry_point: longest_string
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: pick the element with the largest computed value using max(..., key=lambda
    ...)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of strings, return the string that has the most characters. Use `max` with a `key=lambda` to find it.

## Hints
1. Use the built-in `max` function with a `key` argument.
2. The `key` should be a lambda that returns the length of each string.
3. Try: `max(words, key=lambda w: len(w))`
