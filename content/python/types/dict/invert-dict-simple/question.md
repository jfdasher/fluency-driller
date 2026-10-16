---
kind: idiom
status: approved
topic: types/dict
entry_point: invert_dict
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
Write a function `invert_dict` that takes a dictionary and returns a new dictionary with keys and values swapped. You may assume all values are unique and hashable.

## Hints
1. Iterate over the items of the dictionary to access both keys and values.
2. Use a dict comprehension where the new key is the old value and the new value is the old key.
3. Return `{v: k for k, v in d.items()}`.
