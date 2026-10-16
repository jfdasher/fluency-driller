---
kind: idiom
status: approved
topic: operators/boolean
entry_point: get_username
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: guard an expression with short-circuit 'and'
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `get_username(user)` that returns `user.name` if `user` is not `None`, otherwise returns `None`. Use a single short-circuit `and` expression (no `if` statement).

## Hints
1. `and` short-circuits: if the left operand is falsy it is returned immediately without evaluating the right operand.
2. Because `None` is falsy, `user and user.name` will return `None` when `user` is `None`, preventing an `AttributeError`.
3. The full expression is simply `return user and user.name`.
