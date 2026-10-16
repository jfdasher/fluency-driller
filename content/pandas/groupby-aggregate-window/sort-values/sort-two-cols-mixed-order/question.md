---
kind: recall
status: approved
topic: groupby-aggregate-window/sort-values
entry_point: sort_mixed
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: sort by two columns with mixed ascending/descending order
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame sorted by 'dept' ascending and 'salary' descending (keeping the original index).

        dept  salary
     +------+--------+
  0  |   HR |  50000 |
  1  |   IT |  90000 |
  2  |   HR |  70000 |
  3  |   IT |  80000 |
  4  |  OPS |  60000 |

## Hints
1. Use df.sort_values() with the by parameter set to a list of two column names.
2. The ascending parameter accepts a list of booleans, one per column, e.g. [True, False].
3. Call df.sort_values(by=['dept', 'salary'], ascending=[True, False]) to sort dept A→Z and salary high→low.
