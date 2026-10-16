---
kind: idiom
status: approved
topic: types/dict
entry_point: group_words_by_length
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: group values into lists with dict.setdefault
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given a list of words, return a dict mapping each word length (as an int) to a list of words with that length, in the order they appear. Use dict.setdefault to build the groups.

## Hints
1. Iterate over the words and use len(word) as the dict key.
2. dict.setdefault(key, []) returns the existing list if the key exists, or inserts and returns a new empty list.
3. Call result.setdefault(len(word), []).append(word) inside the loop to group words by length.
