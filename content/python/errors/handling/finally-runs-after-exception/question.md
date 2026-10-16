---
kind: recall
status: approved
topic: errors/handling
entry_point: safe_divide
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: guarantee cleanup with a finally clause
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `safe_divide(a, b, log)` that tries to compute `a / b`, appends `'done'` to the list `log` in a `finally` clause (so it always runs), and returns the result. If a `ZeroDivisionError` occurs, catch it and return `None` (but `'done'` must still be appended).

## Hints
1. Use `try/except ZeroDivisionError` to handle division by zero, and add a `finally` block.
2. In the `finally` block, call `log.append('done')`. This runs whether or not an exception was raised.
3. Store the result in a variable before returning so `finally` can still execute; return the variable after the try/except/finally.
