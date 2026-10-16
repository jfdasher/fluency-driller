---
kind: idiom
status: approved
topic: index/reindex-align
entry_point: add_aligned
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: add two Series and rely on automatic index alignment (by label, not
    position)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two Series with overlapping but non-identical integer indices, return a new Series that is their element-wise sum using pandas automatic index alignment (do NOT reset the index or reindex manually — let pandas align by label).

Series `a`:

  index | values
  ------+-------
    1   |  10
    2   |  20
    3   |  30

Series `b`:

  index | values
  ------+-------
    2   |  200
    3   |  300
    4   |  400

Return `a + b` aligned by label; labels present in only one Series become NaN.

## Hints
1. Pandas Series addition automatically aligns on the index labels before computing the sum.
2. When a label exists in only one of the two Series, the result at that label is NaN — this is the expected behavior, not an error.
3. Simply write `return a + b`; pandas handles all index alignment internally without any extra steps.
