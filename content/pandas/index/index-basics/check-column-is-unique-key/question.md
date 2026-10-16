---
kind: idiom
status: approved
topic: index/index-basics
entry_point: check_unique_key
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: test whether a column can serve as a unique key with is_unique
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given the DataFrame `df`, return `True` if the `'id'` column contains all unique values (i.e., can serve as a unique key), and `False` otherwise. Use the pandas `is_unique` property.

```
        id   name
      +----+-------+
  0   |  1 | Alice |
  1   |  2 | Bob   |
  2   |  3 | Carol |
```

For the frame above the answer is `True`; for a frame where `'id'` has a repeated value the answer is `False`.

## Hints
1. Convert the column to an Index or just call a property directly on the Series — both expose `is_unique`.
2. A pandas Series has an `is_unique` property that returns a single bool without needing `.nunique()` or `.duplicated()`.
3. Use `df['id'].is_unique` — it returns `True` when every value in the column appears exactly once.
