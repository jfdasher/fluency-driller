---
kind: idiom
status: approved
topic: numpy-foundations/vectorization
entry_point: add_arrays
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: add two numpy arrays elementwise without a Python loop
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two 1-D NumPy arrays `a` and `b` of the same length, return a new array whose elements are the elementwise sum of `a` and `b` — do NOT use any Python loop.

## Hints
1. NumPy arrays support arithmetic operators directly on the whole array.
2. The `+` operator on two NumPy arrays performs elementwise addition without any explicit loop.
3. Simply write `a + b`; NumPy broadcasts the addition across every element automatically.
