---
kind: recall
status: approved
topic: groupby-aggregate-window/shift-diff-pct
entry_point: add_price_delta
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: compute row-to-row differences down a column with diff
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame with an added column `'delta'` containing the row-to-row difference of the `'price'` column (each row minus the previous row).

```
   price
0   10.0
1   15.0
2   13.0
3   20.0
4   18.0
```

The first row of `'delta'` should be `NaN` (no previous value).

## Hints
1. You need to compute each element minus the element directly above it in the same column.
2. pandas Series has a method that computes the difference between consecutive elements; look for `.diff()`.
3. Call `df['price'].diff()` and assign the result to a new column `'delta'` on a copy of the DataFrame.
