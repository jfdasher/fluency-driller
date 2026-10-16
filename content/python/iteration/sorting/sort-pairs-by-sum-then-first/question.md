---
kind: idiom
status: approved
topic: iteration/sorting
entry_point: sort_pairs_by_sum_then_first
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: double sort with a lambda as the key
  verified:
    ok: false
    attempts: 2
    failures:
    - 'case 0: expected [[1, 1], [1, 3], [2, 2], [0, 4]], got [[1, 1], [0, 4], [1,
      3], [2, 2]]'
    - 'case 1: expected [[1, 5], [2, 4], [3, 3], [0, 6]], got [[0, 6], [1, 5], [2,
      4], [3, 3]]'
---
## Prompt
Given a list of (int, int) tuples, sort them first by the sum of each pair in ascending order, then by the first element of the pair in ascending order when sums are equal. Return the sorted list.

## Hints
1. Use the built-in `sorted()` function with a `key` argument.
2. The key should be a lambda that returns a tuple of two values: the sum and the first element.
3. Use `key=lambda p: (p[0] + p[1], p[0])` to sort by sum first, then by the first element.
