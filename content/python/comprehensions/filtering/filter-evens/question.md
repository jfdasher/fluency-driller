---
kind: idiom
status: approved
topic: comprehensions/filtering
entry_point: keep_evens
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: select a subset with a trailing if-clause, dropping non-matching items
    (not transforming them)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `keep_evens(numbers)` that takes a list of integers and returns a new list containing only the even numbers, using a list comprehension with a trailing `if` clause.

## Hints
1. Use a list comprehension: `[expr for item in iterable if condition]`.
2. The condition to check for even numbers is `n % 2 == 0`.
3. Write `[n for n in numbers if n % 2 == 0]` — the `if` clause drops odd numbers without transforming anything.
