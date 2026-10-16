---
kind: recall
status: approved
topic: functions/lambda
entry_point: keep_evens
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
Write a function `keep_evens(numbers)` that takes a list of integers and returns a list containing only the even numbers, using `filter` and a `lambda`.

## Hints
1. Use `filter()` to select elements from the list that satisfy a condition.
2. `filter(func, iterable)` keeps elements where `func(element)` is truthy; wrap the result in `list()`.
3. The lambda should check divisibility by 2: `lambda x: x % 2 == 0`.
