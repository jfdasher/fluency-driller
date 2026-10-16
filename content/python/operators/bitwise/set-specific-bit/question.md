---
kind: recall
status: approved
topic: operators/bitwise
entry_point: set_bit
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: test and set a specific bit with shifts and masks
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `set_bit(n, k)` that returns the integer `n` with bit `k` (0-indexed from the least significant bit) forced to 1. Use shifts and masks.

## Hints
1. Create a mask with only bit `k` set by computing `1 << k`.
2. Use the bitwise OR operator `|` to set bit `k` in `n` without changing other bits.
3. Return `n | (1 << k)` — OR-ing with the mask guarantees bit `k` becomes 1.
