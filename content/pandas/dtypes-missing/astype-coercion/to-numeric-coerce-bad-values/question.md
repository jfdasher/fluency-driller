---
kind: idiom
status: approved
topic: dtypes-missing/astype-coercion
entry_point: coerce_numeric_column
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: coerce a messy numeric column, turning bad values into NaN with to_numeric(errors='coerce')
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given df with a column `value` that contains a mix of numeric strings and non-numeric garbage, return a new DataFrame with `value` replaced by its numeric equivalent, turning unparseable entries into NaN.

          value
        +-------+
  0     |  '3'  |
  1     | 'abc' |
  2     |  '7'  |
  3     |  '?'  |
  4     | '1.5' |

Return a new DataFrame; do not mutate the input.

## Hints
1. Look at pd.to_numeric and its errors parameter.
2. pd.to_numeric(series, errors='coerce') converts bad values to NaN instead of raising.
3. Assign the result back to the 'value' column of a copy: out['value'] = pd.to_numeric(df['value'], errors='coerce').
