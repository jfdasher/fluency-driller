---
kind: idiom
status: approved
topic: control-flow/with
entry_point: read_file
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: open and read a file using a with-statement context manager
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `read_file(path)` that opens the file at `path` using a `with` statement and returns its entire contents as a string.

## Hints
1. Use `open(path)` inside a `with` block to ensure the file is closed automatically.
2. Inside the `with` block, call `.read()` on the file object to get all contents as a string.
3. The pattern is: `with open(path) as f: return f.read()`
