---
kind: idiom
status: approved
topic: stdlib/json
entry_point: serialize_with_datetime
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: serialize an unsupported type with a default= hook
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `serialize_with_datetime(obj)` that serializes a Python object to a JSON string. If the object (or any nested value) contains a `datetime.datetime` instance, it should be serialized as its ISO 8601 string (e.g. `'2024-01-15T10:30:00'`). Use the `default=` hook in `json.dumps`.

## Hints
1. Pass a callable to the `default=` parameter of `json.dumps`; it is called only for objects that are not natively serializable.
2. Inside the `default` function, check if the value is a `datetime.datetime` instance and return `o.isoformat()` for it.
3. Your `default` hook should raise `TypeError` for any type it does not handle, so that json still reports errors for truly unsupported types.
