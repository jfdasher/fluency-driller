---
kind: idiom
status: approved
topic: comprehensions/basic
entry_point: squares_dict
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a dict with a dict comprehension
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given an integer n, return a dict mapping each integer from 1 to n (inclusive) to its square using a dict comprehension.

## Hints
1. A dict comprehension has the form {key: value for var in iterable}.
2. Use range(1, n+1) to iterate from 1 to n inclusive, and map each i to i*i.
3. return {i: i * i for i in range(1, n + 1)}
