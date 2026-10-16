---
kind: idiom
status: approved
topic: combining/merge-basics
entry_point: inner_join_on_id
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: inner-join two DataFrames on a key column with merge
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two DataFrames `left` and `right`, return a new DataFrame that is the inner join of `left` and `right` on the `'id'` column using `pd.merge`.

`left`:

        id   name
      +----+------+
  0   |  1 | Alice|
  1   |  2 |  Bob |
  2   |  3 | Carol|

`right`:

        id  score
      +----+------+
  0   |  2 |   88 |
  1   |  3 |   95 |
  2   |  4 |   70 |

Only rows where `id` appears in **both** frames are kept.

## Hints
1. Use `pd.merge()` — it accepts two DataFrames and a `on` keyword specifying the key column.
2. Pass `how='inner'` (which is actually the default) to keep only rows whose `id` value exists in both frames.
3. The full call is `pd.merge(left, right, on='id', how='inner')`; the result has columns `id`, `name`, and `score` with two rows (id=2 and id=3).
