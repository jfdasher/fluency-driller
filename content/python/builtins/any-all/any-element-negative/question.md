---
kind: idiom
status: approved
topic: builtins/any-all
entry_point: has_negative
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: check that any element matches with any()
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `has_negative(numbers)` that returns `True` if **any** element in the list is negative, using `any()`.

## Hints
1. Think about what condition each element must satisfy to be considered negative.
2. Use `any()` with a generator expression that checks `x < 0` for each element.
3. Return `any(x < 0 for x in numbers)`.
