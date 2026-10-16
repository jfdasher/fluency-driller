---
kind: idiom
status: approved
topic: types/str-methods
entry_point: parse_csv_line
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: split a comma-separated line and strip whitespace from each field
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `parse_csv_line(line)` that takes a single comma-separated string and returns a list of fields with leading and trailing whitespace removed from each field.

## Hints
1. Split the string on commas first, then process each piece.
2. Use a list comprehension to apply `.strip()` to every element after splitting.
3. Combine `.split(',')` and a list comprehension: `[f.strip() for f in line.split(',')]`.
