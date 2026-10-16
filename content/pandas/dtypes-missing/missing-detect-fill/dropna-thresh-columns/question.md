---
kind: idiom
status: approved
topic: dtypes-missing/missing-detect-fill
entry_point: drop_sparse_columns
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: drop columns with fewer than N non-null values using dropna(axis=1,
    thresh=)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df`, drop any column that has **fewer than 3 non-null values**, returning a new DataFrame.

```
         a     b     c     d
       +-----+-----+-----+-----+
  0    |  1  | NaN |  7  | NaN |
  1    |  2  |  5  |  8  | NaN |
  2    |  3  |  6  |  9  | NaN |
  3    | NaN | NaN | 10  | NaN |
```

Column `a` has 3 non-null values, `b` has 2, `c` has 4, `d` has 0 — so only `a` and `c` survive the threshold of 3.

## Hints
1. Use `df.dropna()` — it accepts an `axis` argument to operate on columns instead of rows.
2. The `thresh` parameter of `dropna` keeps only columns (or rows) that have at least `thresh` non-null values.
3. Call `df.dropna(axis=1, thresh=3)` to retain every column with 3 or more non-null entries.
