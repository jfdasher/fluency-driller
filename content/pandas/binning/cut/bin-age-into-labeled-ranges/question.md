---
kind: idiom
status: approved
topic: binning/cut
entry_point: bin_age
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: bin a continuous column into labeled ranges with cut
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df with an 'age' column of integers, return a new DataFrame with an additional 'age_group' column that bins 'age' into the labeled ranges shown below using `pd.cut` with bins [0, 18, 35, 60, 100] and labels ['youth', 'young_adult', 'middle_aged', 'senior'] (include the left edge only on the rightmost bin, i.e. use the default right=True).

         age
       +-----+
  0    |   5 |
  1    |  22 |
  2    |  45 |
  3    |  70 |
  4    |  18 |

Expected result:

         age   age_group
       +-----+-----------+
  0    |   5 |     youth |
  1    |  22 | young_adult|
  2    |  45 | middle_aged|
  3    |  70 |    senior |
  4    |  18 |     youth |

## Hints
1. Use `pd.cut(df['age'], bins=[0, 18, 35, 60, 100], labels=[...])` to create a Categorical series of labeled intervals.
2. Assign the result of `pd.cut` to a new column on a copy of the DataFrame — remember that 18 falls in the (0, 18] bucket ('youth') because right=True by default.
3. The returned column is a `CategoricalDtype`; construct `expected['age_group']` with `pd.Categorical(..., categories=['youth','young_adult','middle_aged','senior'], ordered=True)` so dtypes match in the test.
