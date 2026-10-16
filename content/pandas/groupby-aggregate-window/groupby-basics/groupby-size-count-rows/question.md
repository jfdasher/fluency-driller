---
kind: recall
status: approved
topic: groupby-aggregate-window/groupby-basics
entry_point: count_rows_per_group
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: count rows per group with groupby().size()
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a Series with the number of rows per 'dept' group using groupby().size().

     dept  score
  0    A     10
  1    B     20
  2    A     30
  3    C     40
  4    B     50
  5    B     60

The result should be a Series named 'dept' (the groupby key becomes the index name) with index ['A','B','C'] and values [2, 3, 1].

## Hints
1. Group the DataFrame by the 'dept' column using df.groupby('dept').
2. After grouping, call .size() on the GroupBy object — it counts rows in each group and returns a Series.
3. df.groupby('dept').size() returns a Series whose index is the unique 'dept' values and whose values are the row counts.
