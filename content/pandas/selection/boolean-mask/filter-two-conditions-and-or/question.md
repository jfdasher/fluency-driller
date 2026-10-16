---
kind: idiom
status: approved
topic: selection/boolean-mask
entry_point: filter_two_conditions
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: filter on two conditions combined with & and | (each parenthesized)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame containing only the rows where `score >= 80` AND `grade == 'A'`, OR where `score >= 95` (regardless of grade). Use `&` and `|` with each condition parenthesized.

         score  grade
       +------+------+
  0    |   72 |  'B' |
  1    |   85 |  'A' |
  2    |   90 |  'B' |
  3    |   96 |  'A' |
  4    |   78 |  'A' |
  5    |   97 |  'C' |

## Hints
1. Wrap each individual condition in parentheses before combining them with `&` or `|`.
2. Build two sub-expressions: `(df['score'] >= 80) & (df['grade'] == 'A')` and `(df['score'] >= 95)`, then join them with `|`.
3. Use `df[mask].reset_index(drop=True)` so the returned DataFrame has a clean 0-based index matching the expected output.
