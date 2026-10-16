---
kind: idiom
status: approved
topic: numpy-foundations/boolean-masking
entry_point: select_positive
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: select the array elements greater than zero with a boolean mask
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a 1-D numpy array `arr`, return a new 1-D array containing only the elements that are strictly greater than zero, preserving their original order.

## Hints
1. Create a boolean array by comparing arr to 0 with the > operator.
2. Use the boolean array directly inside square brackets on arr to index it.
3. arr[arr > 0] applies the boolean mask and returns only the True-indexed elements.
