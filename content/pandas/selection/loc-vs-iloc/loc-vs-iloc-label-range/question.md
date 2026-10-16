---
kind: idiom
status: approved
topic: selection/loc-vs-iloc
entry_point: select_loc_iloc
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: select a label range with .loc (endpoint inclusive) vs positions with
    .iloc (endpoint exclusive)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df` below, select rows whose **index labels** are `'b'` through `'d'` (inclusive) using `.loc`, then select the first two rows using `.iloc` (positions 0 and 1, endpoint exclusive), and return a tuple `(loc_result, iloc_result)` — both as new DataFrames.

```
        value
      +-------+
  a   |   10  |
  b   |   20  |
  c   |   30  |
  d   |   40  |
  e   |   50  |
```

`loc_result` should contain rows `b`, `c`, `d`; `iloc_result` should contain rows `a`, `b`.

## Hints
1. `.loc` uses label-based indexing and its stop label is **inclusive**; `.iloc` uses integer positions and its stop is **exclusive**.
2. For `.loc`, write `df.loc['b':'d']`; for `.iloc`, write `df.iloc[0:2]` to get positions 0 and 1.
3. Return a plain Python tuple: `return (df.loc['b':'d'], df.iloc[0:2])`.
