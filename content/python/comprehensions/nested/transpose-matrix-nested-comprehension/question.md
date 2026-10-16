---
kind: idiom
status: approved
topic: comprehensions/nested
entry_point: transpose
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: transpose a matrix with a nested comprehension
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a 2D list `matrix` (a list of rows, all the same length), return its transpose using a single nested list comprehension — i.e. swap rows and columns.

## Hints
1. The outer comprehension should iterate over column indices, and the inner comprehension should iterate over rows.
2. Use `range(len(matrix[0]))` for the column indices and iterate `for row in matrix` in the inner comprehension.
3. Return `[[row[i] for row in matrix] for i in range(len(matrix[0]))]`.
