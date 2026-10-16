---
kind: recall
status: approved
topic: operators/bitwise
entry_point: is_bit_set
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
Write a function `is_bit_set(n, k)` that returns `True` if bit `k` (0-indexed from the least significant bit) of integer `n` is set (1), and `False` otherwise. Use shifts and masks.

## Hints
1. Shift `n` right by `k` positions to bring bit `k` to the LSB position.
2. After shifting, mask with `1` using `& 1` to isolate the bit.
3. Return `bool((n >> k) & 1)` to convert the isolated bit to a boolean.
