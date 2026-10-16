---
kind: idiom
status: approved
topic: gotchas/copy
entry_point: safe_clone
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: deep-copy a nested list, mutate one inner cell, and leave the original
    unchanged (a shallow copy shares the inner sublists)
  verified:
    ok: false
    attempts: 3
    failures:
    - 'case 0: expected [[[99, 2], [3, 4]], True], got ([[99, 2], [3, 4]], True)'
    - 'case 1: expected [[[99, 8, 9], [10, 11, 12]], True], got ([[99, 8, 9], [10,
      11, 12]], True)'
    - 'case 2: expected [[[99]], True], got ([[99]], True)'
---
## Prompt
Write a function `safe_clone(grid)` that returns a deep copy of the 2-D list `grid` such that modifying any cell of the returned copy does NOT affect `grid`. Return a list `[clone, original_unchanged]` where `clone` is the deep copy (with grid[0][0] set to 99) and `original_unchanged` is a boolean indicating whether `grid[0][0]` is still its original value after the mutation.

## Hints
1. If you use `clone = grid[:]`, then `clone[0]` and `grid[0]` are the same sublist object, so mutating `clone[0][0]` also changes `grid[0][0]`.
2. To make every sublist independent you need a recursive copy — exactly what `copy.deepcopy` provides.
3. Import `copy` and use `copy.deepcopy(grid)` so that inner sublists are also duplicated, making the clone fully independent.
