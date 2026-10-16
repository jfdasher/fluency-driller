---
kind: recall
status: approved
topic: control-flow/with
entry_point: copy_file
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: enter multiple context managers in a single with-statement
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Implement `copy_file(src, dst)` that opens `src` for reading and `dst` for writing using a **single** `with` statement (both context managers on the same line), then copies every line from `src` into `dst`. Return `None`.

## Hints
1. A `with` statement can manage more than one context manager if you separate them with commas.
2. The syntax is `with open(src) as fin, open(dst, 'w') as fout:` — both files are opened and closed together.
3. Use `with open(src, 'r') as fin, open(dst, 'w') as fout:` then iterate over `fin` and call `fout.write(line)`.
