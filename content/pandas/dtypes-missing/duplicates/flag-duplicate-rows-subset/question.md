---
kind: idiom
status: approved
topic: dtypes-missing/duplicates
entry_point: flag_duplicate_rows_subset
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: flag duplicate rows on a subset of key columns with duplicated(subset=)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df`, return a boolean Series (named `is_dup`) that is `True` for every row that is a duplicate based on the `'name'` and `'dept'` columns (keep the first occurrence as `False`).

```
   name     dept   salary
0  Alice    Eng    90000
1  Bob      Mkt    70000
2  Alice    Eng    95000
3  Carol    Eng    80000
4  Bob      Mkt    72000
5  Alice    HR     88000
```

Expected result (a Series named `is_dup`):

```
0    False
1    False
2     True
3    False
4     True
5    False
Name: is_dup, dtype: bool
```

## Hints
1. Use `df.duplicated()` with the `subset` parameter to limit duplicate detection to specific columns.
2. Pass `keep='first'` so that the first occurrence of each combination is marked `False` and subsequent duplicates are marked `True`.
3. The call is `df.duplicated(subset=['name', 'dept'], keep='first')`, then set `.name = 'is_dup'` on the resulting Series.
