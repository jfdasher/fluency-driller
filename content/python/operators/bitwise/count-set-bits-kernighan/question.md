---
kind: idiom
status: approved
topic: operators/bitwise
entry_point: count_set_bits
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
Implement `count_set_bits(n)` that counts the number of 1-bits in the non-negative integer `n` by repeatedly clearing the lowest set bit with the idiom `n & (n - 1)` until `n` becomes zero. Each iteration removes exactly one set bit, so the number of iterations equals the number of set bits.

## Hints
1. Use a loop that continues while `n` is non-zero, updating `n` each iteration.
2. Each application of `n & (n - 1)` removes exactly the lowest set bit; increment a counter each time.
3. The loop body is `n = n & (n - 1)` and you increment a counter; return the counter after the loop.
