---
kind: recall
status: approved
topic: construction-inspection/inspect
entry_point: shape_and_dtypes
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: report the (rows, cols) shape and per-column dtypes of a DataFrame
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given the DataFrame `df` shown below, return a dict with exactly two keys:
- `"shape"`: the tuple `(nrows, ncols)` from `df.shape`
- `"dtypes"`: a `dict` mapping each column name to its dtype object (from `df.dtypes`)

```
        age    score   name
      +------+-------+--------+
  0   |   25 |  88.5 | 'Alice'
  1   |   30 |  92.0 | 'Bob'
  2   |   22 |  79.3 | 'Carol'
```

`age` is int64, `score` is float64, `name` is object.

## Hints
1. Every DataFrame exposes `.shape` as a tuple and `.dtypes` as a Series mapping column names to dtype objects.
2. Convert `.dtypes` to a plain dict with `dict(df.dtypes)` so the return value is a simple Python dict.
3. Return `{"shape": df.shape, "dtypes": dict(df.dtypes)}` — no mutation or copying needed.
