---
kind: idiom
status: approved
topic: types/dict
entry_point: count_digits
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
Write a function `count_digits(n)` that takes a non-negative integer `n` and returns a dictionary mapping each digit character to how many times it appears in the decimal representation of `n`. Use the default fallback idiom.

## Hints
1. Convert the integer to a string so you can iterate over each digit character.
2. Use a dictionary and update each key with `counts.get(ch, 0) + 1` as you iterate.
3. Loop `for ch in str(n):` and set `counts[ch] = counts.get(ch, 0) + 1`, then return `counts`.
