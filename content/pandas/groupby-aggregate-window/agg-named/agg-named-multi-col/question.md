---
kind: idiom
status: approved
topic: groupby-aggregate-window/agg-named
entry_point: agg_multi_col
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: aggregate different columns with different functions in a single agg
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df with columns `dept`, `salary`, and `years`, return a new DataFrame produced by grouping on `dept` and computing three named aggregates in a single `.agg()` call: `avg_salary` = mean of `salary`, `max_salary` = max of `salary`, and `tenure` = mean of `years`. The result should have `dept` as the index.

```
   dept  salary  years
0     A   50000      3
1     A   60000      5
2     B   70000      7
3     B   80000      9
```

Expected result (index name = `dept`):

```
      avg_salary  max_salary  tenure
dept
A        55000.0       60000     4.0
B        75000.0       80000     8.0
```

## Hints
1. Use df.groupby('dept').agg(...) and pass keyword arguments inside agg — each keyword defines an output column name.
2. Each keyword argument should be a tuple of (source_column, aggregation_function), e.g. avg_salary=('salary', 'mean').
3. All three named aggregates go inside a single .agg() call: agg(avg_salary=('salary','mean'), max_salary=('salary','max'), tenure=('years','mean')).
