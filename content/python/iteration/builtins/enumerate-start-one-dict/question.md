---
kind: idiom
status: approved
topic: iteration/builtins
entry_point: index_from_one
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: number items from one with enumerate(seq, start=1)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of strings, return a dict mapping 1-based position numbers (as strings) to the corresponding string, using enumerate with start=1.

## Hints
1. You need to pair each item with a 1-based number — enumerate() can do this.
2. Pass start=1 to enumerate() so counting begins at 1 instead of 0.
3. Use a dict comprehension over enumerate(items, start=1), converting the index to a string for the key.
