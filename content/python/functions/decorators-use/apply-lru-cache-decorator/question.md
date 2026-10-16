---
kind: recall
status: approved
topic: functions/decorators-use
entry_point: slow_square
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: apply a single decorator to a function
  verified:
    ok: true
    attempts: 3
    failures: []
---
## Prompt
Define a function `slow_square(n)` that returns `n * n`. Apply `@functools.lru_cache` so repeated calls with the same argument are cached. Import `functools` inside the function is not allowed; import it at module level in your answer.

## Hints
1. `functools.lru_cache` is a decorator available in the standard library that caches return values.
2. Place `@functools.lru_cache` directly above the `def slow_square(n):` line.
3. The decorator can be applied as `@functools.lru_cache` (no parentheses needed in Python 3.8+).
