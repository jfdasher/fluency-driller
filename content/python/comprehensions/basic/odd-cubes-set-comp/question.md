---
kind: idiom
status: approved
topic: comprehensions/basic
entry_point: odd_cubes
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a set with a set comprehension
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `odd_cubes(n)` that returns a **set** of the cubes of all odd integers in `range(n)`, built with a set comprehension.

## Hints
1. A set comprehension uses `{expr for item in iterable if condition}` syntax.
2. Filter with `if x % 2 != 0` (or `if x % 2 == 1`) to keep only odd numbers.
3. Return `{x**3 for x in range(n) if x % 2 != 0}` — curly braces produce a set.
