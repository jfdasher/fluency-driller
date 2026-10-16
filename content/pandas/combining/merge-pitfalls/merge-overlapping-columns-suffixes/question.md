---
kind: recall
status: approved
topic: combining/merge-pitfalls
entry_point: merge_with_suffixes
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: disambiguate overlapping non-key columns with suffixes
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Two DataFrames share a non-key column name `score`. Merge them on `id` and rename the overlapping columns to `score_left` and `score_right` (left frame first).

Left frame (`left`):

     id  score
   +----+------+
 0 |  1 |   80 |
 1 |  2 |   90 |

Right frame (`right`):

     id  score
   +----+------+
 0 |  1 |   75 |
 1 |  2 |   85 |

Return a new DataFrame with columns `id`, `score_left`, `score_right` (int64 throughout).

## Hints
1. pd.merge() has a `suffixes` parameter that controls what is appended to overlapping column names.
2. Pass `suffixes=('_left', '_right')` to pd.merge() alongside `on='id'` to resolve the name clash.
3. The call is: pd.merge(left, right, on='id', suffixes=('_left', '_right')) — suffixes is a 2-tuple applied to (left, right) overlapping columns.
