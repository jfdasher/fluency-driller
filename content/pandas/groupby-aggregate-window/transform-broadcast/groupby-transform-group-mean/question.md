---
kind: idiom
status: approved
topic: groupby-aggregate-window/transform-broadcast
entry_point: add_group_mean
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: add a column of each row's group mean using groupby().transform
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df`, return a new DataFrame with an added column `'group_mean_score'` containing each row's group mean of `'score'`, grouped by `'category'`. Use `groupby().transform`.

         category  score
       +----------+------+
  0    |   A      |  10  |
  1    |   B      |  20  |
  2    |   A      |  30  |
  3    |   B      |  40  |
  4    |   A      |  50  |

Expected output adds column `group_mean_score`: A rows get 30.0, B rows get 30.0.

## Hints
1. You need each row to carry its group's mean value — this is a broadcast operation, not a reduction.
2. `groupby('category')['score'].transform(...)` returns a Series aligned to the original index, suitable for assigning as a new column.
3. Use `.transform('mean')` (or `.transform(lambda x: x.mean())`) to compute the group mean and broadcast it back to every row in that group.
