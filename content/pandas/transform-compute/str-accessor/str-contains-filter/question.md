---
kind: idiom
status: approved
topic: transform-compute/str-accessor
entry_point: filter_error_rows
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: keep rows whose text column contains a pattern with .str.contains
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df`, return a new DataFrame containing only the rows where the `message` column contains the substring `'error'` (case-insensitive), preserving the original index.

```
          message
       +-----------------------------+
  0    |  'System started normally'  |
  1    |  'ERROR: disk full'         |
  2    |  'warning: low memory'      |
  3    |  'error code 404 returned'  |
  4    |  'All systems operational'  |
       +-----------------------------+
           ^
           +-- index (df.index)
```

Return only the rows at index 1 and 3.

## Hints
1. Use the `.str` accessor on the Series to call string methods element-wise.
2. `.str.contains(pattern)` accepts a `case` keyword argument to control case sensitivity.
3. Pass `case=False` to `.str.contains('error', case=False, na=False)` and use the resulting boolean mask to index into `df`.
