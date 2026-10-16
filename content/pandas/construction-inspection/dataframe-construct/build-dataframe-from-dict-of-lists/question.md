---
kind: recall
status: approved
topic: construction-inspection/dataframe-construct
entry_point: build_dataframe
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a DataFrame from a dict of equal-length column lists
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given three equal-length Python lists, build and return a DataFrame with columns `name`, `age`, and `score` (in that order), using the lists as column data.

The input lists and expected output:

  names  = ['Alice', 'Bob', 'Charlie']
  ages   = [25, 30, 35]
  scores = [88.5, 92.0, 79.3]

  name     age  score
+--------+----+------+
| Alice  | 25 | 88.5 |
| Bob    | 30 | 92.0 |
| Charlie| 35 | 79.3 |

Return a new DataFrame constructed from those three lists.

## Hints
1. You can pass a plain Python dict to the pd.DataFrame constructor, where each key becomes a column name and its value (a list) provides the column data.
2. Construct the dict with keys in the desired column order: {'name': names, 'age': ages, 'score': scores}, then wrap it with pd.DataFrame(...).
3. The one-liner is: return pd.DataFrame({'name': names, 'age': ages, 'score': scores})
