---
kind: recall
status: approved
topic: classes/basics
entry_point: Point
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: define a class with __init__ and instance attributes
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Define a class `Point` with an `__init__` method that accepts `x` and `y` and stores them as instance attributes.

## Hints
1. Use `self` as the first parameter in `__init__` to refer to the instance being created.
2. Assign each parameter to the instance using `self.x = x` inside `__init__`.
3. Both attributes must be stored with `self.x = x` and `self.y = y` so they are accessible on the object later.
