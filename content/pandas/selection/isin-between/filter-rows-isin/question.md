---
kind: idiom
status: approved
topic: selection/isin-between
entry_point: filter_rows_isin
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: keep rows whose category is in a set of allowed values with isin
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame containing only the rows where the 'category' column is one of the allowed values `{'B', 'D'}`.

```
   category  value
0         A     10
1         B     20
2         C     30
3         D     40
4         B     50
5         A     60
```

Expected result:

```
   category  value
1         B     20
3         D     40
4         B     50
```

## Hints
1. Boolean-index df with a condition on the 'category' column.
2. Series.isin() accepts any iterable of allowed values and returns a boolean mask.
3. Use `df[df['category'].isin({'B', 'D'})]` to keep only rows whose category is B or D.
