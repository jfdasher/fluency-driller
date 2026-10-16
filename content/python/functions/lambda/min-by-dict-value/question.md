---
kind: idiom
status: approved
topic: functions/lambda
entry_point: lowest_scorer
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: find the element with the smallest computed value using min(..., key=lambda
    ...)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a dictionary mapping names (strings) to scores (integers), return the name of the person with the lowest score.

## Hints
1. Iterating over a dict yields its keys; use `min()` on the dict directly.
2. `min()` accepts a `key=` argument — use it to look up each key's value in the dict.
3. Pass `key=lambda name: scores[name]` so `min()` compares by score rather than by name.
