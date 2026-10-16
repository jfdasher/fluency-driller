---
kind: recall
status: approved
topic: numpy-foundations/vectorization
entry_point: scale_array
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: scale every element of an array by a scalar via broadcasting
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a 1-D NumPy array `arr` and a scalar `factor`, return a **new** array where every element has been multiplied by `factor` using NumPy broadcasting (no Python loops).

Example:

    arr    = [1, 2, 3, 4, 5]
    factor = 3
    result = [3, 6, 9, 12, 15]

## Hints
1. NumPy overloads the `*` operator so that multiplying an array by a scalar applies the operation to every element automatically.
2. The expression `arr * factor` returns a brand-new array; the original `arr` is left unchanged.
3. Broadcasting means NumPy 'stretches' the scalar to match the shape of the array, so `arr * factor` is all you need — no loops required.
