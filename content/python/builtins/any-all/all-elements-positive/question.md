---
kind: idiom
status: approved
topic: builtins/any-all
entry_point: all_positive
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: check that all elements satisfy a predicate with all()
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `all_positive(numbers)` that returns `True` if every number in the list is positive (greater than zero), using `all()`.

## Hints
1. Use a generator expression inside `all()` to test each element.
2. `all(expr for x in iterable)` returns True only when every element satisfies `expr`.
3. Return `all(x > 0 for x in numbers)`.
