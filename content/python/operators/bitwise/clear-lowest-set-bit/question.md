---
kind: idiom
status: approved
topic: operators/bitwise
entry_point: clear_lowest_set_bit
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
Implement `clear_lowest_set_bit(n)` that returns the integer `n` with its lowest set bit cleared, using the single bitwise idiom `n & (n - 1)`. For example, `clear_lowest_set_bit(6)` should return `4` (binary `110` -> `100`).

## Hints
1. Think about what subtracting 1 does to the binary representation of n.
2. Subtracting 1 from n flips the lowest set bit to 0 and all lower bits to 1; ANDing with n cancels those bits.
3. The one-liner is simply `return n & (n - 1)`.
