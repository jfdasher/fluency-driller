---
kind: idiom
status: approved
topic: comprehensions/filtering
entry_point: clamp_negatives
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: transform every item with a conditional ternary in the comprehension's
    value position, keeping all items (not dropping any)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `clamp_negatives(nums)` that takes a list of numbers and returns a new list where every negative number is replaced with 0, and every non-negative number is kept as-is. Use a list comprehension with a ternary expression in the value position (keep ALL items).

## Hints
1. You need to keep every element, just transforming some of them — so don't filter with `if` at the end of the comprehension.
2. Use a ternary: `value_if_true if condition else value_if_false` as the expression part of the comprehension.
3. The expression should be `x if x >= 0 else 0` for each `x` in `nums`.
