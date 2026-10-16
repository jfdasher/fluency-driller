---
kind: recall
status: approved
topic: functions/lambda
entry_point: uppercase_all
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: transform each item with map and a lambda
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Use `map` and a `lambda` to return a list where every string in `words` is converted to uppercase.

## Hints
1. `map` applies a function to each element of an iterable and returns a map object.
2. A lambda that uppercases a string looks like `lambda w: w.upper()`.
3. Convert the map object to a list: `list(map(lambda w: w.upper(), words))`.
