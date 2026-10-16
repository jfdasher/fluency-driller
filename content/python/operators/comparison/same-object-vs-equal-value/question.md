---
kind: idiom
status: approved
topic: operators/comparison
entry_point: same_object
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: choose 'is' for identity vs '==' for equality
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Implement two functions: `same_object(a, b)` that returns `True` only when `a` and `b` are the **same object** (identity), and `equal_value(a, b)` that returns `True` when `a` and `b` have **equal values** (equality). Use `is` for the first and `==` for the second.

## Hints
1. `is` compares object identity (same memory address); `==` compares object value via `__eq__`.
2. Two lists `[1, 2]` and `[1, 2]` are equal in value but are **not** the same object.
3. Use `a is b` in `same_object` and `a == b` in `equal_value`.
