---
kind: recall
status: approved
topic: construction-inspection/dataframe-construct
entry_point: build_df
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: construct a DataFrame with an explicit index and column order
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given the data dictionary below, construct a DataFrame whose **rows** appear in the order `['c', 'a', 'b']` and whose **columns** appear in the order `['score', 'name']`.

Data dictionary:

    data = {
        'name':  {'a': 'Alice', 'b': 'Bob',   'c': 'Carol'},
        'score': {'a': 90,      'b': 85,       'c': 95}
    }

Expected result:

           score   name
         +-------+-------+
    c    |   95  | Carol |
    a    |   90  | Alice |
    b    |   85  | Bob   |

Write `build_df(data)` that returns this DataFrame (index name should be `None`).

## Hints
1. Pass both `index=` and `columns=` keyword arguments to `pd.DataFrame()`.
2. The `index` parameter controls row order; pass `['c', 'a', 'b']` to reorder the rows away from insertion order.
3. Call `pd.DataFrame(data, index=['c', 'a', 'b'], columns=['score', 'name'])` — pandas selects and reorders both axes simultaneously.
