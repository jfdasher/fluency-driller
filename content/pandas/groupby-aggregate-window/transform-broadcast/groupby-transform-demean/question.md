---
kind: idiom
status: approved
topic: groupby-aggregate-window/transform-broadcast
entry_point: demean_by_group
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: center each value by subtracting its group mean with transform
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame with a single column `'value_demeaned'` containing each `'value'` minus its group mean (grouped by `'group'`), preserving the original row order and index.

      group  value
    +-------+------+
  0 |  'A'  |  10  |
  1 |  'B'  |  20  |
  2 |  'A'  |  30  |
  3 |  'B'  |  40  |
  4 |  'A'  |  50  |

Group means: A = 30.0, B = 30.0
Expected result:

     value_demeaned
    +--------------+
  0 |   -20.0      |
  1 |   -10.0      |
  2 |     0.0      |
  3 |    10.0      |
  4 |    20.0      |

## Hints
1. Use `groupby` on the `'group'` column and select `'value'`, then call `.transform('mean')` to broadcast the group mean back to every row.
2. Subtract the result of `.transform('mean')` from `df['value']` element-wise — this preserves the original index and row order automatically.
3. `df['value'] - df.groupby('group')['value'].transform('mean')` gives the demeaned values; wrap in `pd.DataFrame({'value_demeaned': ...})` to produce the required output.
