---
kind: idiom
status: approved
topic: types/str-methods
entry_point: join_words
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: join a list of words with a separator string
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `join_words(words, sep)` that takes a list of strings `words` and a separator string `sep`, and returns a single string with all words joined by the separator.

## Hints
1. Think about which object you call the join method on.
2. The separator string itself has a `.join()` method that accepts an iterable.
3. Use `sep.join(words)` to produce the result.
