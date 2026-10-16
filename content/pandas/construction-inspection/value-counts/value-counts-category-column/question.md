---
kind: idiom
status: approved
topic: construction-inspection/value-counts
entry_point: count_colors
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: count occurrences of each category in a column with value_counts
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a DataFrame `df` with a column `'color'`, return a Series with the count of each unique value in `'color'`, sorted by count descending (ties broken by the value alphabetically ascending).

```
   color
0    red
1   blue
2    red
3  green
4   blue
5    red
```

Expected result (a Series named `'color'`):

```
color
red      3
blue     2
green    1
Name: count, dtype: int64
```

## Hints
1. Use the `value_counts()` method on a Series to get occurrence counts sorted descending by default.
2. To break ties alphabetically, first sort by the index (the category values), then do a stable sort by count descending so equal counts stay in alphabetical order.
3. Chain: `df['color'].value_counts().sort_index().sort_values(ascending=False, kind='stable')`
