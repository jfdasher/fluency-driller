---
kind: idiom
status: approved
topic: groupby-aggregate-window/agg-named
entry_point: named_group_agg
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: produce several named per-group aggregates in one agg call (named
    aggregation)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df` with columns `dept`, `salary`, and `years`, return a new DataFrame (one row per department) with three columns computed in a single `.agg()` call using named aggregation:
- `avg_salary`: mean of `salary`
- `max_years`: max of `years`
- `headcount`: count of `salary`

The result should be indexed by `dept`.

      dept  salary  years
  0     HR   50000      3
  1     HR   60000      5
  2    Eng   90000      7
  3    Eng  110000     10
  4    Eng   95000      4
  5  Sales   45000      2

Expected result (index name = 'dept'):

         avg_salary  max_years  headcount
  dept
  Eng      98333.33         10          3
  HR       55000.00          5          2
  Sales    45000.00          2          1

## Hints
1. Use `df.groupby('dept').agg(...)` and pass keyword arguments where each key is the new column name.
2. Each keyword argument in `.agg()` takes a tuple `(column_name, aggregation_function)`, e.g. `avg_salary=('salary', 'mean')`.
3. The full call is: `df.groupby('dept').agg(avg_salary=('salary','mean'), max_years=('years','max'), headcount=('salary','count'))`.
