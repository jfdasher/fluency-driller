---
kind: idiom
status: approved
topic: types/tuple
entry_point: distance_from_origin
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: use a namedtuple for readable field access
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Define a namedtuple `Point` with fields `x` and `y`. Write a function `make_point(x, y)` that returns a `Point` instance, and a function `distance_from_origin(p)` that takes a `Point` and returns the Euclidean distance from (0, 0) using named field access (p.x, p.y).

## Hints
1. Use `collections.namedtuple('Point', ['x', 'y'])` to define the Point type.
2. Access fields with `p.x` and `p.y` rather than `p[0]` and `p[1]`.
3. Return `math.sqrt(p.x**2 + p.y**2)` using named field access for clarity.
