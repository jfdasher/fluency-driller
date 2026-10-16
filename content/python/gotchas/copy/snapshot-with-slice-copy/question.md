---
kind: idiom
status: approved
topic: gotchas/copy
entry_point: record_snapshots
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: append a running snapshot cur[:] each loop step so captured states
    stay independent (without [:] they all alias the final list)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
You are building a step-by-step recorder. Given a list of integers `ops` (each op is appended one-by-one to a running accumulator), return a list of snapshots where each snapshot is the state of the accumulator after adding that element. Use `cur[:]` (a slice copy) when capturing each snapshot so that earlier snapshots are not overwritten by later mutations.

## Hints
1. Build up a single list `cur` and append to it each iteration, then save the current state into `snapshots`.
2. If you write `snapshots.append(cur)`, every entry in `snapshots` will point to the same list object and all will reflect the final state — use a copy instead.
3. Use `cur[:]` (slice copy) when appending to `snapshots` so each captured state is an independent list: `snapshots.append(cur[:])`.
