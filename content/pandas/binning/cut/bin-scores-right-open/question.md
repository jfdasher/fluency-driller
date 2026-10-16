---
kind: recall
status: approved
topic: binning/cut
entry_point: bin_scores
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: bin values into custom edges with right-open intervals (right=False)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a DataFrame with a 'score' column, add a 'grade' column by binning 'score' into the right-open intervals [0,60), [60,70), [70,80), [80,90), [90,100] with labels ['F','D','C','B','A'] using `pd.cut` (right=False, include_lowest=True).

     score
   +-------+
 0 |    55 |
 1 |    60 |
 2 |    75 |
 3 |    85 |
 4 |    95 |
 5 |     0 |

Return a new DataFrame with both 'score' and 'grade' columns.

## Hints
1. Use `pd.cut` with a list of bin edges and a matching `labels` list.
2. Pass `right=False` so intervals are left-closed/right-open (e.g. [60,70)), and `include_lowest=True` so the leftmost edge 0 is included.
3. `pd.cut(df['score'], bins=[0,60,70,80,90,100], labels=['F','D','C','B','A'], right=False, include_lowest=True)` gives the Categorical 'grade' column.
