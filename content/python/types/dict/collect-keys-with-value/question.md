---
kind: recall
status: approved
topic: types/dict
entry_point: keys_with_value
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: iterate keys, values, and items via dict views
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a dict mapping string keys to integers and a target integer value, return a sorted list of all keys whose value equals the target. Use dict.items() to iterate over the dict.

## Hints
1. Iterate over the dict using a view that gives you access to both keys and values simultaneously.
2. Use dict.items() to unpack each entry as (k, v), then check if v == target to collect matching keys.
3. Build the list with a generator expression: sorted(k for k, v in d.items() if v == target).
