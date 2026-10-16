---
kind: recall
status: approved
topic: groupby-aggregate-window/sort-values
entry_point: sort_by_score_desc
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: sort a DataFrame by a column in descending order with sort_values
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame sorted by the 'score' column in descending order (highest first), resetting nothing — keep the original index labels.

       name  score
  0   Alice     82
  1     Bob     95
  2   Carol     70
  3   David     95
  4     Eve     88

The result should have rows ordered from highest to lowest score; rows with equal scores should appear in their original relative order (stable sort).

## Hints
1. Use the pandas DataFrame method that reorders rows based on column values.
2. sort_values accepts an `ascending` keyword argument — set it to False for descending order.
3. Call df.sort_values('score', ascending=False, kind='stable') and return the result directly without resetting the index.
