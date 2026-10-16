---
kind: recall
status: approved
topic: transform-compute/str-accessor
entry_point: split_full_name
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: split a text column on a delimiter with .str.split
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df with a 'full_name' column, return a new DataFrame with two columns 'first' and 'last' created by splitting 'full_name' on a single space.

  full_name (df.columns)
+-----------+
| Alice Bob |
| Carol Dee |
| Eve Fox   |

Expected result:

  first  last
+-------+-----+
| Alice | Bob |
| Carol | Dee |
| Eve   | Fox |

## Hints
1. Use the .str accessor on the 'full_name' Series to access string methods.
2. Call .str.split(' ', expand=True) to get a DataFrame of split pieces instead of a Series of lists.
3. Index into the resulting DataFrame with [0] and [1] to get the first and last name columns, then assemble a new DataFrame with keys 'first' and 'last'.
