---
kind: recall
status: approved
topic: dtypes-missing/missing-detect-fill
entry_point: fill_score
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: fill missing values in a column with a constant via fillna
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame where every NaN in column 'score' is replaced with 0 (as a float).

         name   score
       +------+-------+
  0    | Alice |   NaN |
  1    |   Bob |   8.5 |
  2    | Carol |   NaN |
  3    | David |   7.0 |

Leave all other columns unchanged.

## Hints
1. Use Series.fillna() on the 'score' column and assign the result into a copy of the DataFrame.
2. df.copy() gives you a new DataFrame; then out['score'] = df['score'].fillna(value) replaces only the NaNs.
3. The full solution is: out = df.copy(); out['score'] = df['score'].fillna(0.0); return out
