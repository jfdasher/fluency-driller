---
kind: idiom
status: approved
topic: selection/boolean-mask
entry_point: filter_above_threshold
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: filter rows where a column exceeds a threshold with a boolean mask
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df`, return a new DataFrame containing only the rows where the `score` column is strictly greater than `threshold`.

             name  score
           +------+------+
  0        | Alice|   82 |
  1        |  Bob |   55 |
  2        | Carol|   91 |
  3        | Dave |   70 |
           ^
           +-- index (df.index)

For example, with threshold=70 the result keeps rows 0 and 2 (scores 82 and 91).

## Hints
1. Build a boolean Series by comparing df['score'] to the threshold, then use it to index into df.
2. Use df[df['score'] > threshold] to select matching rows; call .reset_index(drop=True) so the returned frame has a clean 0-based index.
3. The one-liner is: return df[df['score'] > threshold].reset_index(drop=True)
