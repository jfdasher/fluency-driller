---
kind: recall
status: approved
topic: selection/loc-vs-iloc
entry_point: select_rows_cols
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: select specific rows and columns by label with .loc[rows, cols]
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df`, use `.loc` to select rows with labels `'b'` and `'d'`, keeping only columns `'x'` and `'z'`, and return the result as a new DataFrame.

```
        x    y    z      <- columns
      +----+----+----+
  a   |  1 |  2 |  3 |
  b   |  4 |  5 |  6 |
  c   |  7 |  8 |  9 |
  d   | 10 | 11 | 12 |
  ^
  +-- index
```

## Hints
1. Use `.loc[row_labels, col_labels]` to select by label on both axes simultaneously.
2. Pass a list of row labels as the first argument and a list of column labels as the second argument to `.loc`.
3. The exact call is `df.loc[['b', 'd'], ['x', 'z']]`.
