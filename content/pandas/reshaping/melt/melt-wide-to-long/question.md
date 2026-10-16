---
kind: idiom
status: approved
topic: reshaping/melt
entry_point: melt_scores
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: reshape wide measure columns into long form with melt (id_vars, value_vars)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, reshape it from wide to long form by melting the measure columns `q1`, `q2`, `q3` into two columns `quarter` and `score`, keeping `student` as the identifier.

        student   q1   q2   q3   <- columns
       +--------+----+----+----+
  0    | Alice  | 85 | 90 | 78 |
  1    | Bob    | 72 | 68 | 95 |
    ^
    +-- index (default RangeIndex)

Return a new DataFrame with columns `student`, `quarter`, `score` (in that order), reset to a default RangeIndex.

## Hints
1. Use pd.DataFrame.melt() with id_vars='student' and value_vars=['q1','q2','q3'] to unpivot the frame.
2. Pass var_name='quarter' and value_name='score' to name the new indicator and value columns correctly.
3. Call .reset_index(drop=True) on the result so the returned frame has a clean default RangeIndex.
