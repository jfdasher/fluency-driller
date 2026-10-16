---
kind: idiom
status: approved
topic: selection/chained-assignment
entry_point: promote_seniors
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: assign to a filtered subset with .loc[mask, col] = value
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df`, return a **new** DataFrame where the `'status'` column is set to `'senior'` for every row where `'age'` is 65 or older, leaving all other values unchanged.

```
        age  status
     +-----+--------+
  0  |  23 | junior |
  1  |  67 | junior |
  2  |  65 | junior |
  3  |  41 | junior |
  4  |  70 | junior |
```

Expected result:

```
        age  status
     +-----+--------+
  0  |  23 | junior |
  1  |  67 | senior |
  2  |  65 | senior |
  3  |  41 | junior |
  4  |  70 | senior |
```

## Hints
1. Make a copy of `df` first so the original is not mutated, then work on the copy.
2. Use `.loc[mask, col] = value` where `mask` is a boolean Series — this is the idiomatic single-step filtered assignment.
3. Build the mask as `out['age'] >= 65`, then write `out.loc[mask, 'status'] = 'senior'` on the copy before returning it.
