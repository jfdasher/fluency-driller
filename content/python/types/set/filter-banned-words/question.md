---
kind: idiom
status: approved
topic: types/set
entry_point: remove_banned
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: test membership in O(1) with a set instead of a list scan
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of banned words and a list of words from a message, return a new list containing only the words that are NOT banned. Use a set for the banned-word lookup.

## Hints
1. Build a set from the banned list so each membership check is O(1) instead of O(n).
2. Use a list comprehension that keeps words where `w not in banned_set`.
3. Convert banned to a set first: `banned_set = set(banned)`, then filter with `[w for w in words if w not in banned_set]`.
