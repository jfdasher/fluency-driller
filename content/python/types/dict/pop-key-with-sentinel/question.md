---
kind: recall
status: approved
topic: types/dict
entry_point: drop_key
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: remove a key safely with dict.pop and a default
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `drop_key(d, key, default)` that removes `key` from dictionary `d` using `dict.pop` with the given `default` value, and returns whatever `dict.pop` returns. The dictionary should be mutated in place.

## Hints
1. Use `dict.pop` so that missing keys do not raise a KeyError.
2. `dict.pop(key, default)` returns `default` when the key is absent.
3. Simply return `d.pop(key, default)` directly.
