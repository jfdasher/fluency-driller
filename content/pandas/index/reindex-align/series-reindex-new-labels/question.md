---
kind: idiom
status: approved
topic: index/reindex-align
entry_point: reindex_series
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: conform a Series to a new index with reindex, filling absent labels
    with NaN
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a Series `s`, reindex it to `new_index`, filling any absent labels with NaN. Return the resulting Series.

`s`:

            value   <- Series name
          +-------+
  alpha   |  10.0 |
  beta    |  20.0 |
  gamma   |  30.0 |
    ^
    +-- index

`new_index` = ['alpha', 'gamma', 'delta', 'epsilon']

Expected result:

            value
          +-------+
  alpha   |  10.0 |
  gamma   |  30.0 |
  delta   |   NaN |
  epsilon |   NaN |

## Hints
1. Look at the pandas Series method that conforms a Series to a new index.
2. The method is called `reindex`; absent labels are automatically filled with NaN by default.
3. Use `s.reindex(new_index)` — this returns a new Series aligned to `new_index` with NaN for any label not present in `s`.
