---
kind: idiom
status: approved
topic: iteration/builtins
entry_point: lists_to_dict
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: pair two lists element-wise with zip
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of `keys` and a list of `values`, return a dictionary mapping each key to its corresponding value by zipping the two lists together.

## Hints
1. You need to associate each key with the value at the same position.
2. `zip` pairs elements from two iterables; passing the result to `dict()` creates a mapping.
3. Use `dict(zip(keys, values))` directly.
