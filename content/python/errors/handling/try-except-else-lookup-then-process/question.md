---
kind: idiom
status: approved
topic: errors/handling
entry_point: get_processed
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: narrow the protected block using try/except/else
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Implement `get_processed(d, key)` that looks up `d[key]` in the narrowest possible try block, catches `KeyError` by returning `None`, and — only if the lookup succeeded — uppercases the value and returns it from the `else` clause. The `.upper()` call must NOT be inside the `try` block.

## Hints
1. Use try/except/else so the else clause only executes when no KeyError was raised.
2. Only the dictionary lookup `d[key]` belongs in the try block; `.upper()` goes in else.
3. The pattern is: try: value = d[key]   except KeyError: return None   else: return value.upper()
