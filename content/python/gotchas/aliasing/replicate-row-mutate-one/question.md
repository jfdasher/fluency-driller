---
kind: idiom
status: approved
topic: gotchas/aliasing
entry_point: replicate_row_mutate_one
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: replicate a given row m times then change one copy — the [row]*m trap
    mutates every copy
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Create a grid of `m` rows each initialised to a copy of `row`, then set the element at index `col` in row 0 to `val`. Return the resulting grid. Every other row must remain unchanged.

## Hints
1. Building the grid with `[row] * m` makes every row the same object; mutating one mutates all.
2. Use a loop or list comprehension to create each row independently, e.g. `[list(row) for _ in range(m)]`.
3. Each row must be a fresh copy: `list(row)` (or `row[:]`) inside the comprehension gives independent lists.
