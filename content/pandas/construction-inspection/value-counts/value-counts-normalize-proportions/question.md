---
kind: idiom
status: approved
topic: construction-inspection/value-counts
entry_point: proportions
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: get category proportions with value_counts(normalize=True)
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given a Series `s` of string labels, return a new Series of the relative frequency (proportion) of each value, sorted descending by proportion, with float64 dtype.

Example input `s`:

  0    cat
  1    dog
  2    cat
  3    cat
  4    dog
  dtype: object

Expected output (a Series):

  cat    0.6
  dog    0.4
  dtype: float64

Use `value_counts(normalize=True)` to compute proportions.

## Hints
1. Call `.value_counts()` on the Series — it has a keyword argument that switches from counts to fractions.
2. The keyword argument is `normalize=True`; when set, each count is divided by the total length of the Series.
3. Return `s.value_counts(normalize=True)` directly — this gives a float64 Series sorted descending with label names as the index.
