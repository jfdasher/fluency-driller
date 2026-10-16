---
kind: idiom
status: approved
topic: functions/lambda
entry_point: highest_score
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
Given a list of dicts, each with a 'score' key, return the dict that has the highest 'score'. Use `max` with a `key=lambda` to find it.

## Hints
1. Use the built-in `max` function with a `key` argument.
2. The `key` should be a lambda that extracts the 'score' from each dict.
3. Try: `max(records, key=lambda r: r['score'])`
