---
kind: recall
status: approved
topic: control-flow/while
entry_point: is_prime
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: use a while-else clause
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Implement `is_prime(n)` that returns `True` if `n` is a prime number and `False` otherwise. Use a `while`-`else` clause: trial-divide starting from 2 up to (but not including) `n`; if a divisor is found break out and skip the `else`; the `else` block (no divisor found) should return `True`. Numbers less than 2 are not prime.

## Hints
1. The `else` clause of a `while` loop executes when the condition becomes False naturally (not via `break`). Use `break` when a divisor is found.
2. You only need to check divisors up to the square root of `n`. The `else` block fires when `i * i > n` without hitting `break`.
3. Pattern: `while i * i <= n: if n % i == 0: break; i += 1` then `else: return True` then `return False` (reached only after a break).
