---
kind: recall
status: approved
topic: functions/signatures
entry_point: collect_args
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: accept arbitrary positional and keyword args with *args/**kwargs
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `collect_args` that accepts any number of positional arguments and any number of keyword arguments, and returns a tuple of (args_tuple, kwargs_dict).

## Hints
1. Use *args to capture all positional arguments as a tuple.
2. Use **kwargs to capture all keyword arguments as a dict.
3. Return them together as a two-element tuple: (args, kwargs).
