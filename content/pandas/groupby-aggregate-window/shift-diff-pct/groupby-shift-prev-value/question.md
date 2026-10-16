---
kind: idiom
status: approved
topic: groupby-aggregate-window/shift-diff-pct
entry_point: add_prev_value
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: get the previous row's value within each group with groupby().shift
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df with columns 'group' and 'value', return a new DataFrame with an added column 'prev_value' containing the previous row's value within each group (NaN for the first row in each group), preserving row order.

  group  value
+-------+------+
|  A    |  10  |
|  A    |  20  |
|  A    |  30  |
|  B    |  100 |
|  B    |  200 |
+-------+------+

Expected output:

  group  value  prev_value
+-------+------+-----------+
|  A    |  10  |   NaN     |
|  A    |  20  |  10.0     |
|  A    |  30  |  20.0     |
|  B    |  100 |   NaN     |
|  B    |  200 | 100.0     |
+-------+------+-----------+

## Hints
1. Within each group you need the value from the row directly above — pandas has a shift operation that can be applied per group.
2. Use groupby('group')['value'] to get a GroupBy object on the value column, then call .shift(1) to lag by one position.
3. df.groupby('group')['value'].shift(1) returns a Series aligned to the original index; assign it as a new column on a copy of df.
