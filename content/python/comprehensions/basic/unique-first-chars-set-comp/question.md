---
kind: idiom
status: approved
topic: comprehensions/basic
entry_point: unique_first_chars
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a set with a set comprehension
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `unique_first_chars(words)` that takes a list of non-empty strings and returns a **set** of the first character of each word, built with a set comprehension.

## Hints
1. A set comprehension looks like a list comprehension but uses curly braces `{}`.
2. Index into each word with `word[0]` to get its first character.
3. Return `{word[0] for word in words}` — the braces (not brackets) make it a set.
