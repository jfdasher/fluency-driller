---
kind: idiom
status: approved
topic: gotchas/aliasing
entry_point: set_cell
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build an m×n grid of zeros, set one cell, and return it — the [[0]*n]*m
    trap corrupts the whole column
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `set_cell(m, n, row, col, val)` that creates an m×n grid of zeros (list of lists), sets grid[row][col] to val, and returns the grid. Every other cell must remain 0. Do NOT use the `[[0]*n]*m` pattern.

## Hints
1. Using `[[0]*n]*m` creates m references to the same inner list, so setting any cell corrupts the entire column.
2. Build each row independently so they are distinct objects in memory.
3. Use a list comprehension: `[[0] * n for _ in range(m)]` to create m separate row lists.
