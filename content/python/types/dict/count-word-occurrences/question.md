---
kind: idiom
status: approved
topic: types/dict
entry_point: count_words
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: count occurrences with counts.get(key, 0) + 1
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `count_words(words)` that takes a list of strings and returns a dictionary mapping each word to the number of times it appears in the list. Use the default fallback idiom (do not use `collections.Counter`).

## Hints
1. Build an empty dict and iterate through the list, updating each word's count.
2. `dict.get(key, default)` returns the current count or 0 if the key is missing; add 1 to that result.
3. Inside the loop: `counts[word] = counts.get(word, 0) + 1`.
