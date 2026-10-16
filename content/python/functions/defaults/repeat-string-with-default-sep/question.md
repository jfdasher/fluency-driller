---
kind: recall
status: approved
topic: functions/defaults
entry_point: call_with_dot
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: override a single keyword-defaulted parameter by name, leaving the
    other defaults unchanged
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Define a function `repeat_str(text, times=3, sep='-')` that returns the string `text` repeated `times` times, joined by `sep` (e.g., `repeat_str('hi')` → `'hi-hi-hi'`). Then define `call_with_dot()` that calls `repeat_str` overriding only `sep` to `'.'` for `text='ab'`, leaving `times` at its default.

## Hints
1. Keyword arguments can be passed in any order; unspecified ones keep their defaults.
2. Call `repeat_str('ab', sep='.')` — `times` will remain 3.
3. Use `sep='.'` by name so Python uses the default `times=3` automatically.
