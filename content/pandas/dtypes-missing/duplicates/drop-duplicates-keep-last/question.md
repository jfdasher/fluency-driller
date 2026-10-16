---
kind: recall
status: approved
topic: dtypes-missing/duplicates
entry_point: drop_duplicates_keep_last
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: keep the last occurrence of each duplicate with keep='last'
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame that keeps only the **last** occurrence of each duplicate row based on the `'city'` column, preserving original index values.

```
        city   temp
      +------+------+
  0   |  NYC |   70 |
  1   |  LAX |   85 |
  2   |  NYC |   72 |
  3   |  LAX |   88 |
  4   |  CHI |   60 |
```

Expected result (last occurrences, original index retained):

```
        city   temp
      +------+------+
  2   |  NYC |   72 |
  3   |  LAX |   88 |
  4   |  CHI |   60 |
```

## Hints
1. Use the `.drop_duplicates()` method on the DataFrame.
2. Pass `subset='city'` to consider only the city column when detecting duplicates.
3. Set `keep='last'` to retain the final occurrence of each duplicated city value.
