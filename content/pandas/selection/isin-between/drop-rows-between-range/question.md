---
kind: idiom
status: approved
topic: selection/isin-between
entry_point: drop_between
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: drop rows whose value falls inside a range using ~between
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given `df`, return a new DataFrame containing only the rows where `score` does NOT fall in the closed interval [40, 70] (i.e. drop every row where 40 ≤ score ≤ 70).

```
        score
      +-------+
  0   |   25  |
  1   |   55  |
  2   |   40  |
  3   |   85  |
  4   |   70  |
  5   |   10  |
  6   |   60  |
```

Expected result keeps rows 0, 3, 5 (scores 25, 85, 10).

## Hints
1. Use pandas Series.between(low, high) to create a boolean mask of rows inside the range.
2. Negate the mask with ~ to select rows OUTSIDE the range, then filter df with df[mask].
3. Chain everything: df[~df['score'].between(40, 70)].reset_index(drop=True)
