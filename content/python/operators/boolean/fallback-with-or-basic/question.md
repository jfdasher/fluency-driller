---
kind: idiom
status: approved
topic: operators/boolean
entry_point: get_username
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: supply a fallback value with 'or'
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Implement `get_username(name)` that returns `name` if it is truthy, otherwise returns the string `'Anonymous'`.

## Hints
1. Python's `or` operator returns the first truthy operand, or the last operand if none are truthy.
2. You can write this as a single return statement using `or` without any `if` statement.
3. Try: `return name or 'Anonymous'`
