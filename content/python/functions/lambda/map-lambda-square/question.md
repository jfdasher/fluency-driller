---
kind: recall
status: approved
topic: functions/lambda
entry_point: square_all
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
Use `map` and a `lambda` to return a list where each integer in `nums` is squared.

## Hints
1. The built-in `map(func, iterable)` applies `func` to every element.
2. A lambda that squares its argument looks like `lambda x: x ** 2`.
3. Wrap the result in `list()`: `list(map(lambda x: x ** 2, nums))`.
