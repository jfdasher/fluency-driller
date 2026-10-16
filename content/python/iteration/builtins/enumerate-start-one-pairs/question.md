---
kind: idiom
status: approved
topic: iteration/builtins
entry_point: number_items
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: number items from one with enumerate(seq, start=1)
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given a list of strings, return a list of (number, string) tuples where numbering starts at 1, using enumerate with start=1.

## Hints
1. Use the built-in enumerate() function to pair each item with its position.
2. enumerate() accepts a second argument that sets the starting counter value.
3. Call enumerate(items, start=1) and convert the result to a list.
