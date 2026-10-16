---
kind: idiom
status: approved
topic: numpy-foundations/boolean-masking
entry_point: replace_negatives_with_zero
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: replace negative values with zero using np.where
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a 1-D numpy array `arr`, return a new array of the same shape where every negative value is replaced with 0 and all non-negative values are kept unchanged. Use `np.where`.

Example:

  arr = [ 3, -1,  0,  4, -7,  2]

Expected result:

  out = [ 3,  0,  0,  4,  0,  2]

## Hints
1. Think about a condition you can evaluate element-wise on `arr` that is True wherever you want 0 and False elsewhere.
2. `np.where(condition, x, y)` returns `x` where condition is True, otherwise `y` — map your condition to pick between 0 and the original value.
3. Use `np.where(arr < 0, 0, arr)` to replace every negative element with 0 while keeping the rest.
