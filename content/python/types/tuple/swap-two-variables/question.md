---
kind: idiom
status: approved
topic: types/tuple
entry_point: swap
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: swap two variables with tuple unpacking
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `swap(a, b)` that returns the two values with their positions swapped, using tuple unpacking in a single assignment statement.

## Hints
1. Python allows multiple assignment targets on the left side of `=`.
2. You can unpack a tuple on the right-hand side: `x, y = y, x` swaps x and y in one line.
3. Use `a, b = b, a` then return `a, b`.
