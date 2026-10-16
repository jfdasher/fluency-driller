---
kind: idiom
status: approved
topic: gotchas/mutable-defaults
entry_point: collect_items
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: fix a function whose default [] accumulates across calls
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
The function `collect_items` below has a mutable default argument bug: calling it multiple times accumulates items across calls. Fix it so each call without an explicit `items` argument starts with a fresh empty list.

## Hints
1. The default `[]` is created once when the function is defined, not on each call.
2. Use a sentinel default value like `None` instead of `[]`.
3. Set `items = []` inside the function body when `items is None`.
