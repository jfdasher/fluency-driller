---
kind: recall
status: approved
topic: functions/decorators-use
entry_point: greet
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: stack two decorators on one function
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Two decorators are provided: `uppercase` (converts a string return value to upper case) and `bold` (wraps a string return value in `**...**`). Stack them on a function `greet(name)` that returns `'hello ' + name`, so that calling `greet('world')` returns `'**HELLO WORLD**'`. Apply `bold` as the outermost decorator and `uppercase` as the innermost.

## Hints
1. In Python, stacking decorators means the bottom-most decorator (closest to the function) is applied first.
2. Writing `@bold` above `@uppercase` above `def greet` is equivalent to `greet = bold(uppercase(greet))`.
3. Make sure `greet` returns `'hello ' + name`; `uppercase` will capitalise it, then `bold` will wrap in `**...**`.
