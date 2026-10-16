---
kind: idiom
status: approved
topic: types/dict
entry_point: count_chars
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
Write a function `count_chars(s)` that takes a string `s` and returns a dictionary mapping each character to the number of times it appears in the string. Use the default fallback idiom (do not use `collections.Counter`).

## Hints
1. Iterate over each character in the string and keep a running tally in a dict.
2. Use `counts.get(ch, 0)` to safely retrieve the current count even when the key doesn't exist yet.
3. Inside the loop: `counts[ch] = counts.get(ch, 0) + 1`.
