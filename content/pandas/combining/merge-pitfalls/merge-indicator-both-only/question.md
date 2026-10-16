---
kind: idiom
status: approved
topic: combining/merge-pitfalls
entry_point: ids_in_both
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: diagnose which keys matched with merge(indicator=True)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two DataFrames `left` and `right`, merge them on `'id'` with `how='outer'` and `indicator=True`, then return a **Series** of the `'id'` values (sorted ascending, reset index dropped) that appeared in **both** tables — i.e. where `_merge == 'both'`.

```
left                right
   id  val_l           id  val_r
+----+------+       +----+------+
|  1 |  'a' |       |  1 |  'x' |
|  2 |  'b' |       |  3 |  'y' |
|  3 |  'c' |       |  5 |  'z' |
```

Return a `Series` of dtype int64 containing the `id` values that matched in both tables (here: `[1, 3]`).

## Hints
1. Use `pd.merge(..., how='outer', indicator=True)` to get a `_merge` column with values `'left_only'`, `'right_only'`, or `'both'`.
2. After merging, filter rows where `_merge == 'both'` and select the `'id'` column, then sort and reset the index.
3. Chain: `merged.loc[merged['_merge'] == 'both', 'id'].sort_values().reset_index(drop=True)`.
