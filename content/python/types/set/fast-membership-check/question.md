---
kind: idiom
status: approved
topic: types/set
entry_point: is_allowed
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
Given a list of allowed usernames and a username to look up, return True if the username is in the allowed list, False otherwise. Use a set for the membership test (not a list scan).

## Hints
1. Converting a list to a set allows O(1) average membership testing.
2. Use set(allowed) to create a set, then use the `in` operator.
3. Return `username in set(allowed)`.
