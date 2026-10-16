---
kind: recall
status: approved
topic: iteration/builtins
entry_point: reverse_sequence
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: iterate a sequence backwards with reversed()
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Use `reversed()` to return a new list containing the elements of `items` in reverse order (do not use slicing or `.reverse()`).

## Hints
1. The built-in `reversed()` returns an iterator that yields elements from back to front.
2. Wrap the call in `list()` to materialise the reversed iterator into a list.
3. `list(reversed(items))` is the idiomatic one-liner.
