---
kind: recall
status: approved
topic: construction-inspection/dataframe-construct
entry_point: build_dataframe_from_list_of_dicts
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a DataFrame from a list of row records (list of dicts)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of row records (list of dicts), construct and return a DataFrame where each dict becomes one row.

Input records:
  [ {"name": "Alice", "age": 30, "score": 88.5},
    {"name": "Bob",   "age": 25, "score": 92.0},
    {"name": "Carol", "age": 35, "score": 76.3} ]

Expected result (default RangeIndex 0-2, columns in insertion order):

       name  age  score
     +------+----+------+
  0  | Alice|  30| 88.5 |
  1  | Bob  |  25| 92.0 |
  2  | Carol|  35| 76.3 |

## Hints
1. Think about what pandas constructor accepts a list of dicts directly.
2. pd.DataFrame() can accept many input shapes — a list of dicts is one of the most common.
3. Call pd.DataFrame(records) where records is the list of dicts; each dict's keys become column names.
