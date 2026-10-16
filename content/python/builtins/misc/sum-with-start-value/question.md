---
kind: recall
status: approved
topic: builtins/misc
entry_point: sum_with_offset
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: sum numbers with a non-zero start value
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Use the built-in `sum()` function with a non-zero start value to compute the total of a list of numbers plus an initial offset. Write a function `sum_with_offset(numbers, offset)` that returns `sum(numbers)` plus `offset` using a single call to `sum()`.

## Hints
1. The built-in `sum()` accepts a second argument.
2. `sum(iterable, start)` adds `start` to the total before summing the iterable.
3. Call `sum(numbers, offset)` — the second positional argument to `sum` is the starting value.
