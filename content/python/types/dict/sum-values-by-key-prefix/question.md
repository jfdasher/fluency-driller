---
kind: recall
status: approved
topic: types/dict
entry_point: filter_a_keys
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
Given a dict mapping string keys to integer values, return a new dict containing only the items whose key starts with the letter 'a', preserving the original key-value pairs. Use dict.items() to iterate.

## Hints
1. You need both keys and values from the dict — consider which view gives you both at once.
2. Use dict.items() in a for loop or comprehension to unpack each key-value pair as (k, v).
3. Write {k: v for k, v in d.items() if k.startswith('a')} to keep only entries whose key begins with 'a'.
