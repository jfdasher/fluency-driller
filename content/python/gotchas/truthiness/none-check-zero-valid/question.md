---
kind: idiom
status: approved
topic: gotchas/truthiness
entry_point: get_value
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: use 'if x is not None' when 0 or '' are valid values
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `get_value(data, key, default)` that returns `data[key]` if the key exists in the dict and its value is not None, otherwise returns `default`. It must treat 0 and '' as valid (non-default) values.

## Hints
1. Think about what happens when you write `if data.get(key)` and the value is 0.
2. Use `is not None` instead of a bare truthiness check to distinguish between 'missing/None' and 'falsy but present'.
3. The correct guard is `if val is not None: return val` so that 0, '', and False are all returned as-is.
