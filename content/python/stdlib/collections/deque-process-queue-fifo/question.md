---
kind: idiom
status: approved
topic: stdlib/collections
entry_point: process_tasks
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: use collections.deque.popleft() as an O(1) queue
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function that takes a list of tasks (strings) and a list of cancellations (strings). Process the tasks in FIFO order using a collections.deque with popleft(), skipping any task that appears in the cancellations set. Return the list of processed tasks in order.

## Hints
1. Use collections.deque(tasks) to create the queue, and popleft() to remove tasks in FIFO order.
2. Convert cancellations to a set for O(1) membership checks before appending to result.
3. Loop while the deque is non-empty: popleft() each task, check against the cancelled set, and append to result if not cancelled.
