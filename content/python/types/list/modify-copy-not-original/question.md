---
kind: idiom
status: approved
topic: types/list
entry_point: append_to_copy
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: copy a list with [:] instead of aliasing it
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given a list `data`, use the `[:]` slice idiom to make a copy, append the value `99` to the copy, and return a tuple `(original_data, modified_copy)`. The original list must remain unchanged.

## Hints
1. If you write `copy = data` and then append to `copy`, `data` will also be modified because they point to the same object.
2. Create a true copy first using slice notation, then safely mutate only the copy.
3. Use `copy = data[:]` to get an independent list, then `copy.append(99)` and return `(data, copy)`.
