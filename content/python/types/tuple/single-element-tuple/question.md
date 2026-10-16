---
kind: recall
status: approved
topic: types/tuple
entry_point: make_singleton
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: write a single-element tuple with a trailing comma
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `make_singleton(x)` that returns a single-element tuple containing `x`. Use a tuple literal with a trailing comma, not the `tuple()` constructor.

## Hints
1. A tuple is not created by parentheses alone; `(x)` is just `x`.
2. Adding a trailing comma inside the parentheses tells Python it is a tuple: `(x,)`.
3. The correct literal is `(x,)` — the comma is what makes it a tuple.
