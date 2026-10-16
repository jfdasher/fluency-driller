---
kind: idiom
status: approved
topic: numpy-foundations/vectorization
entry_point: exceeds_threshold
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: compute a boolean array of which elements exceed a threshold
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a 1-D NumPy array `arr` and a scalar `threshold`, return a new boolean NumPy array of the same shape where each element is `True` if the corresponding element of `arr` exceeds `threshold`, and `False` otherwise.

Example:

  arr       = [1, 5, 3, 8, 2]
  threshold = 4
  result    = [False, True, False, True, False]

## Hints
1. Think about what Python comparison operators do when applied directly to a NumPy array.
2. NumPy arrays support element-wise comparisons: `arr > threshold` applies the `>` operator to every element simultaneously without a Python loop.
3. Simply return `arr > threshold`; NumPy broadcasts the scalar and produces a boolean array of the same shape.
