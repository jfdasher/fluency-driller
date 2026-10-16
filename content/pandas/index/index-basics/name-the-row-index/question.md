---
kind: recall
status: approved
topic: index/index-basics
entry_point: name_row_index
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: give a DataFrame's row index a name
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df`, return a new DataFrame whose row index has the name `"student_id"` (the data and columns must be unchanged).

```
        score  grade
      +-------+------+
  0   |    88 |  B   |
  1   |    95 |  A   |
  2   |    72 |  C   |
```

The returned frame should look like:

```
               score  grade
student_id
      +-------+------+
  0   |    88 |  B   |
  1   |    95 |  A   |
  2   |    72 |  C   |
```

where `df.index.name == "student_id"`.

## Hints
1. Every pandas Index object has a `.name` attribute you can read or set.
2. Make a copy of `df` first, then assign to `out.index.name`.
3. Set `out.index.name = "student_id"` on the copied frame before returning it.
