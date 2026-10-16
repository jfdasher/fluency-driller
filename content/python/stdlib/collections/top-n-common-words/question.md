---
kind: idiom
status: approved
topic: stdlib/collections
entry_point: top_n_common_words
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: get the n most common items with Counter.most_common
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given a list of words and an integer n, return the n most common words along with their counts as a list of (word, count) tuples, ordered from most to least common. Use Counter.most_common.

## Hints
1. Counter can be constructed directly from a list and will count occurrences automatically.
2. Counter has a method most_common(n) that returns the top n elements as a list of (element, count) tuples.
3. Just do: Counter(words).most_common(n)
