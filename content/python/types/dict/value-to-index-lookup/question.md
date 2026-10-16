---
kind: idiom
status: approved
topic: types/dict
entry_point: value_to_index
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a value-to-index lookup map from a list
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of unique strings, build a dictionary that maps each string to its index in the list.

## Hints
1. You need to pair each element with its position in the list.
2. Use enumerate() to get both index and value, then build a dict comprehension.
3. The comprehension should map value -> index: {v: i for i, v in enumerate(items)}.
