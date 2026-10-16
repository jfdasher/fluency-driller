---
kind: idiom
status: approved
topic: stdlib/heapq
entry_point: schedule_jobs
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: order a heap by a tuple priority key
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
You have a list of jobs, each as a dict with keys 'priority' (int), 'arrival' (int), and 'name' (str). Schedule them using heapq so that jobs are processed by ascending priority, breaking ties by ascending arrival time. Return the list of job names in processing order.

## Hints
1. Store each job as a (priority, arrival, name) tuple so heapq sorts by priority first, then arrival, then name.
2. Build the list of tuples, call heapq.heapify(), then heappop() each tuple and collect the name.
3. The key insight is that Python tuple comparison is lexicographic, so (priority, arrival, name) gives you the exact tie-breaking you need automatically.
