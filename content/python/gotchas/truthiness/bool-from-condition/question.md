---
kind: idiom
status: approved
topic: gotchas/truthiness
entry_point: is_positive
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: replace 'True if cond else False' with the boolean directly
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Rewrite the function `is_positive(n)` so it returns whether `n` is greater than zero. Do NOT use `if`/`else` or a ternary expression; return the boolean value of the comparison directly.

## Hints
1. A comparison like `n > 0` already produces a bool in Python.
2. You can return the result of a comparison expression directly with `return n > 0`.
3. `True if n > 0 else False` is redundant; `n > 0` is already `True` or `False`.
