---
kind: recall
status: approved
topic: operators/unpacking
entry_point: logged_call
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: forward *args and **kwargs through a wrapper call
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `logged_call(fn, *args, **kwargs)` that calls `fn` with all the forwarded positional and keyword arguments and returns its result. Do not modify the arguments in any way.

## Hints
1. You need to capture extra positional args with `*args` and extra keyword args with `**kwargs` in the wrapper signature.
2. To forward them, unpack both collections when calling `fn`: use `*args` for positional and `**kwargs` for keyword arguments.
3. The call should look like `fn(*args, **kwargs)` — unpack both inside the call to `fn`.
