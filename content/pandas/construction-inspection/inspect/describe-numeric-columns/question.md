---
kind: recall
status: approved
topic: construction-inspection/inspect
entry_point: describe_numeric
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: summarize the numeric columns of a DataFrame with describe
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df`, return the descriptive statistics summary produced by calling `.describe()` on it (all numeric columns, default behaviour).

```
       score  attempts
     +-------+---------+
  0  |  85.0 |       3 |
  1  |  92.0 |       1 |
  2  |  78.0 |       4 |
  3  |  95.0 |       2 |
```

Return the DataFrame that `.describe()` produces (8 summary rows: count, mean, std, min, 25%, 50%, 75%, max).

## Hints
1. Pandas DataFrames have a built-in method that computes summary statistics for numeric columns.
2. The method name is `.describe()` and by default it targets numeric columns only.
3. Call `df.describe()` and return its result directly — no additional arguments needed.
