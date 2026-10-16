---
kind: idiom
status: approved
topic: dtypes-missing/missing-detect-fill
entry_point: count_missing
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: count missing values per column with isna().sum()
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a Series containing the count of missing values in each column.

```
        age   score   name
      +-----+-------+------+
  0   | NaN |   8.5 | 'Alice'
  1   |  25 |   NaN | 'Bob'
  2   |  30 |   7.0 |  NaN
  3   | NaN |   NaN | 'Dana'
```

The result should be a Series indexed by column name with the count of NaN values per column.

## Hints
1. Use a boolean mask that marks missing values, then aggregate.
2. pandas has a built-in method `.isna()` that returns a boolean DataFrame of the same shape.
3. Chain `.isna()` with `.sum()` — summing a boolean DataFrame column-wise counts the True values per column.
