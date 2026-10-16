---
kind: idiom
status: approved
topic: numpy-foundations/boolean-masking
entry_point: zero_out_even_positions
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: zero out masked positions in place with arr[mask] = 0
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a 1-D NumPy array `arr`, return a **new** array where every element at an even index (0, 2, 4, …) is replaced with 0 and all other elements are unchanged.

Example:

  arr  = [10, 21, 30, 41, 50]
  result = [ 0, 21,  0, 41,  0]

## Hints
1. Create a copy of the array first, then build a boolean mask that is True at even indices.
2. You can build the mask with `mask = np.zeros(len(arr), dtype=bool); mask[::2] = True` and then assign `out[mask] = 0`.
3. Use slice notation `[::2]` on a boolean mask array to set every other position to True, then apply `arr[mask] = 0` on the copy.
