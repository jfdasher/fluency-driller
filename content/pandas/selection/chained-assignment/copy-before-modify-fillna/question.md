---
kind: idiom
status: approved
topic: selection/chained-assignment
entry_point: fill_score
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: work on a copy so the original frame is untouched (copy first)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame where the 'score' column has all NaN values replaced with 0, leaving the original frame untouched.

         name  score
       +------+------+
  0    | 'Alice' | NaN  |
  1    | 'Bob'   | 88.0 |
  2    | 'Carol' | NaN  |
  3    | 'Dave'  | 95.0 |

## Hints
1. Make a defensive copy of the DataFrame before modifying any column to avoid mutating the caller's object.
2. Call df.copy() first, then assign to the copied frame's 'score' column using Series.fillna(0).
3. out = df.copy(); out['score'] = out['score'].fillna(0); return out — this pattern is the standard idiom for safe in-place-style edits.
