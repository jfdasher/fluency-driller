---
kind: idiom
status: approved
topic: types/dict
entry_point: group_numbers_by_parity
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: group values into lists with dict.setdefault
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of integers, return a dict with exactly two keys, 'even' and 'odd', each mapping to a list of numbers with that parity in the order they appear. Use dict.setdefault to build the groups.

## Hints
1. Determine whether each number is even or odd to decide its group key ('even' or 'odd').
2. dict.setdefault(key, []) will create a new list for a key the first time it is seen.
3. Use result.setdefault('even' if n % 2 == 0 else 'odd', []).append(n) inside the loop.
