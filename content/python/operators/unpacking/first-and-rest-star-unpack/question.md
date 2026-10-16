---
kind: idiom
status: approved
topic: operators/unpacking
entry_point: first_and_rest
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: split a list into first and rest with star unpacking
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `first_and_rest(lst)` that takes a non-empty list and returns a tuple `(first, rest)` where `first` is the first element and `rest` is a list of the remaining elements. Use star unpacking in a single assignment.

## Hints
1. You can unpack a list into named variables on the left-hand side of an assignment.
2. The `*` prefix on a variable in an unpacking expression collects all remaining items into a list.
3. Use `first, *rest = lst` then return `(first, rest)`.
