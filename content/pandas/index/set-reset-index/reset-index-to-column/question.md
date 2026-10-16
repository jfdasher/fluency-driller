---
kind: recall
status: approved
topic: index/set-reset-index
entry_point: reset_named_index
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: flatten the index back into a regular column with reset_index
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df` with a named index, return a new DataFrame with the index flattened back into a regular column (the index becomes the first column, and the resulting index is the default 0-based integer index).

```
         score
       +-------+
name   |       |
Alice  |    85 |
Bob    |    92 |
Carol  |    78 |
  ^
  +-- index (df.index.name = 'name')
```

Expected result:

```
    name  score
  +------+------+
0 | Alice|   85 |
1 |  Bob |   92 |
2 | Carol|   78 |
```

## Hints
1. You need to move the index back into a column — look for a DataFrame method that is the inverse of `set_index`.
2. The method `reset_index()` converts the current index into a column and restores a default integer index.
3. Call `df.reset_index()` (no arguments needed here); it returns a new DataFrame with the named index as the first column.
