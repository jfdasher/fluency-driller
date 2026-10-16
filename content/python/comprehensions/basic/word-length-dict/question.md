---
kind: idiom
status: approved
topic: comprehensions/basic
entry_point: word_lengths
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
Given a list of strings, return a dict mapping each string to its length using a dict comprehension.

## Hints
1. A dict comprehension looks like {key_expr: value_expr for item in iterable}.
2. Use each word as the key and len(word) as the value.
3. return {word: len(word) for word in words}
