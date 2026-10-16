---
kind: recall
status: approved
topic: functions/decorators-use
entry_point: MathUtils
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: apply a single decorator to a function
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Define a class `MathUtils` with a method `add` that takes two arguments `a` and `b` and returns their sum. Apply the built-in `@staticmethod` decorator so that `MathUtils.add(3, 4)` works without an instance.

## Hints
1. Static methods do not receive `self` or `cls` as their first argument.
2. Place the decorator on the line immediately above the `def` statement using `@staticmethod`.
3. The decorator syntax is `@staticmethod` on the line before `def add(a, b):`.
