---
kind: recall
status: approved
topic: dtypes-missing/missing-detect-fill
entry_point: drop_rows_with_any_na
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: drop rows that have any missing value with dropna
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame containing only the rows that have **no** missing values (drop any row with at least one NaN).

```
     a     b     c
  +-----+-----+-----+
0 | 1.0 | 2.0 | 3.0 |
1 | NaN | 5.0 | 6.0 |
2 | 7.0 | NaN | 9.0 |
3 |10.0 |11.0 |12.0 |
```

Rows 1 and 2 each contain a NaN, so the result keeps only rows 0 and 3.

## Hints
1. pandas DataFrames have a method specifically for dropping missing values — look for `dropna`.
2. `df.dropna()` by default drops rows (`axis=0`) where **any** value is NaN; that default is exactly what you need here.
3. Call `df.dropna()` (no extra arguments needed) and return the result; it returns a new DataFrame and does not mutate the original.
