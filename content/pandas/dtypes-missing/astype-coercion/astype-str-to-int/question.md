---
kind: recall
status: approved
topic: dtypes-missing/astype-coercion
entry_point: cast_val_to_int
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: convert a column of clean numeric strings to int with astype
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df with a column `'val'` containing clean numeric strings, return a new DataFrame where `'val'` is cast to `int64` using `astype`.

```
     val
   +-----+
 0 | '3' |
 1 | '7' |
 2 | '1' |
   +-----+
        ^
        string (object dtype)
```

The returned frame must have `'val'` as `int64` and leave the input unchanged.

## Hints
1. Make a copy of the DataFrame first so you don't mutate the input, then operate on the copy's column.
2. Series.astype accepts a dtype string like `'int64'` or the numpy type `np.int64`.
3. Assign back to the column: `out['val'] = df['val'].astype('int64')` then return `out`.
