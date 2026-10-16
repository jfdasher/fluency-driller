---
kind: recall
status: approved
topic: stdlib/json
entry_point: json_round_trip
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: round-trip a structure with json.dumps and json.loads
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `json_round_trip(obj)` that serializes `obj` to a JSON string with `json.dumps` and immediately deserializes it back with `json.loads`, returning the result.

## Hints
1. You need to import the `json` standard library module.
2. Use `json.dumps(obj)` to convert the object to a JSON string, then pass that string to `json.loads`.
3. Return `json.loads(json.dumps(obj))`.
