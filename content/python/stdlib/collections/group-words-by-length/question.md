---
kind: idiom
status: approved
topic: stdlib/collections
entry_point: group_words_by_length
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: group items with defaultdict(list)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of words, return a dict mapping each word length (as a string key) to the list of words with that length, in the order they appear. Use `defaultdict(list)` to build the grouping.

## Hints
1. Create a `defaultdict(list)` and iterate over the words, using `len(word)` as the key.
2. For each word, do `groups[str(len(word))].append(word)` — no need to check if the key exists first.
3. Convert the result to a plain dict with `dict(groups)` before returning so the output matches the expected type.
