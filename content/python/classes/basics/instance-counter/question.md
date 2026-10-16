---
kind: idiom
status: approved
topic: classes/basics
entry_point: Widget
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: share state across instances with a class attribute
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Define a class `Widget` with a class attribute `count` (initially 0) that tracks how many instances have been created. Each call to `__init__` should increment `Widget.count`. Include a class method `get_count` that returns the current count.

## Hints
1. A class attribute is defined directly on the class body, not inside __init__.
2. Inside __init__, increment the class attribute using `Widget.count += 1` (or `cls.__class__.count += 1`).
3. Use `@classmethod` with `cls` as the first parameter and return `cls.count`.
