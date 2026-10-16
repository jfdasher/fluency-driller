---
kind: recall
status: approved
topic: types/tuple
entry_point: get_x_y
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: unpack a coordinate tuple into named variables
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `get_x_y(coord)` that takes a tuple `(x, y)` and returns the x and y values as a plain Python tuple `(x, y)` by unpacking the input into named variables `x` and `y` first.

## Hints
1. You can assign multiple variables at once from a tuple on a single line.
2. Try writing `x, y = coord` to unpack the tuple into named variables.
3. Use tuple unpacking: `x, y = coord`, then `return (x, y)`.
