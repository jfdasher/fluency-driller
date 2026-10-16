---
kind: recall
status: approved
topic: functions/defaults
entry_point: rectangle_area
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: give a function several default parameters and supply only the first
    positionally
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Define a function `rectangle_area(width, height=10, scale=1)` that returns `width * height * scale`. Call it with only `width` supplied positionally to verify the defaults work.

## Hints
1. Default parameters let callers omit trailing arguments.
2. With only `width` provided, `height` defaults to 10 and `scale` defaults to 1.
3. Simply return `width * height * scale`.
