---
kind: idiom
status: approved
topic: operators/bitwise
entry_point: is_power_of_two
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: clear the lowest set bit with n & (n - 1)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a positive integer `n`, return `True` if `n` is a power of two and `False` otherwise. Use the bit-clearing idiom `n & (n - 1)` to implement this in a single expression.

## Hints
1. A power of two has exactly one set bit; clearing the lowest set bit should leave zero.
2. If `n & (n - 1)` equals 0, then n had only one set bit — which means it's a power of two.
3. Return `n > 0 and (n & (n - 1)) == 0`.
