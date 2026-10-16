---
kind: idiom
status: approved
topic: comprehensions/nested
entry_point: make_grid
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: initialize an m-by-n grid with [[0]*n for _ in range(m)]
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `make_grid(m, n)` that returns an m-by-n grid (list of m lists, each containing n zeros) using a list comprehension. Each row must be an independent list.

## Hints
1. Use a list comprehension with `range(m)` to create m rows.
2. Each row should be `[0] * n` to get n zeros; put this inside the comprehension.
3. The full idiom is `[[0] * n for _ in range(m)]` — the loop variable is unused, so name it `_`.
