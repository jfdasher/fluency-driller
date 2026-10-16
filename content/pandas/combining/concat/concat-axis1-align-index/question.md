---
kind: idiom
status: approved
topic: combining/concat
entry_point: concat_side_by_side
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: glue two frames side-by-side aligning on the index with concat(axis=1)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two DataFrames `left` and `right` that share some index labels, glue them side-by-side (axis=1) using `pd.concat` so that rows align on the shared index and unmatched rows are filled with NaN.

`left`:

        val_a
      +------+
  a   |  1   |
  b   |  2   |
  c   |  3   |

`right`:

        val_b
      +------+
  b   | 20   |
  c   | 30   |
  d   | 40   |

Return the combined DataFrame (index labels a, b, c, d; columns val_a, val_b).

## Hints
1. Use `pd.concat` with a list of the two frames.
2. Pass `axis=1` to stack frames horizontally instead of vertically.
3. Index alignment is automatic; unmatched labels get NaN — no extra arguments needed.
