---
kind: idiom
status: approved
topic: control-flow/for
entry_point: index_and_value_pairs
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: iterate with enumerate instead of range(len(x))
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given a list of strings `words`, return a list of tuples `(index, word)` for every word in the list. Use `enumerate` instead of `range(len(words))`.

## Hints
1. You need both the position and the value of each element — Python has a built-in that gives you both at once.
2. `enumerate(words)` yields `(index, value)` pairs on each iteration; unpack them directly in the loop.
3. Use `[(i, word) for i, word in enumerate(words)]` to build the result list.
