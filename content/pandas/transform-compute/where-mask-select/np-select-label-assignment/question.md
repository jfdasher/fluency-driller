---
kind: idiom
status: approved
topic: transform-compute/where-mask-select
entry_point: assign_grade
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: assign one of several labels by condition with np.select
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame with an additional column `'grade'` assigned by these conditions (in order):
- score >= 90  → `'A'`
- score >= 75  → `'B'`
- score >= 60  → `'C'`
- otherwise    → `'F'`

Use `np.select` to compute the labels.

        score
      +-------+
  0   |   95  |
  1   |   82  |
  2   |   67  |
  3   |   55  |
  4   |   90  |

## Hints
1. Build a list of boolean conditions and a matching list of choice labels, then pass them to np.select along with a default.
2. np.select(conditions, choices, default='F') evaluates conditions in order and returns the first matching choice; assign the result to a new column on a copy of df.
3. conditions = [df['score'] >= 90, df['score'] >= 75, df['score'] >= 60]; choices = ['A', 'B', 'C']; out['grade'] = np.select(conditions, choices, default='F')
