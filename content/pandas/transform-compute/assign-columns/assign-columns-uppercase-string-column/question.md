---
kind: recall
status: approved
topic: transform-compute/assign-columns
entry_point: uppercase_name_column
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: overwrite a column with a transformed version of itself
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df`, return a new DataFrame with the `'name'` column replaced by its uppercased version (all strings converted to upper case). Leave all other columns unchanged.

```
        name   score
      +------+-------+
  0   | alice |    85 |
  1   | bob   |    92 |
  2   | carol |    78 |
```

Expected result:

```
        name   score
      +-------+-------+
  0   | ALICE |    85 |
  1   | BOB   |    92 |
  2   | CAROL |    78 |
```

## Hints
1. Use `.str` accessor methods to apply string operations element-wise on a Series.
2. pandas Series has a `.str.upper()` method that uppercases every element.
3. Copy the DataFrame first, then assign `out['name'] = df['name'].str.upper()` and return `out`.
