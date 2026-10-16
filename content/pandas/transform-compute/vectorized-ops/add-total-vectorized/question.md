---
kind: idiom
status: approved
topic: transform-compute/vectorized-ops
entry_point: add_total
grader: python
modality: code
provenance:
  model: opus-4.8
  source_topic: add a total column with a vectorized Series addition
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a DataFrame `df` with integer columns `a` and `b`, return a NEW DataFrame with an added column `total` equal to the elementwise sum `a + b`. Use a vectorized Series addition — no `apply`, no `iterrows`, no Python loop. Do not mutate the input.

## Hints
1. Column arithmetic is vectorized: `df["a"] + df["b"]` returns a Series aligned on the index.
2. Copy first so you never mutate the caller's frame: `out = df.copy()`.
3. `out = df.copy(); out["total"] = df["a"] + df["b"]; return out`.
