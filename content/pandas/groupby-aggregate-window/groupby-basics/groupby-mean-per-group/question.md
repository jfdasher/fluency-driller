---
kind: recall
status: approved
topic: groupby-aggregate-window/groupby-basics
entry_point: groupby_mean
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: compute the mean of a column per group with groupby
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a Series with the mean of `score` for each `team`, indexed by `team` and named `score`.

         team  score
       +------+------+
  0    |   A  |  10  |
  1    |   B  |  20  |
  2    |   A  |  30  |
  3    |   B  |  40  |
  4    |   A  |  20  |

Expected result (Series):

  team
  A    20.0
  B    30.0
  Name: score

## Hints
1. Use df.groupby() to group by the 'team' column before aggregating.
2. Select the 'score' column after groupby, then call .mean() on it.
3. df.groupby('team')['score'].mean() returns a Series indexed by 'team' with the mean score per group.
