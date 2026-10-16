---
kind: idiom
status: approved
topic: types/dict
entry_point: invert_mapping
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: invert a dict, swapping keys and values
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Write a function `invert_mapping` that takes a dictionary mapping category names (strings) to numeric codes (integers) and returns a new dictionary mapping each numeric code back to its category name.

## Hints
1. Think of the original dict's values (codes) becoming the new dict's keys.
2. A dict comprehension that iterates over `.items()` and swaps the roles of name and code will work.
3. Return `{code: name for name, code in mapping.items()}`.
