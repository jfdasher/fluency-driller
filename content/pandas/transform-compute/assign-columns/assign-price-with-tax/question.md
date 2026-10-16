---
kind: idiom
status: approved
topic: transform-compute/assign-columns
entry_point: add_price_with_tax
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: add a derived column inside a chain with .assign
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df` with columns `price` (float) and `tax_rate` (float), return a **new** DataFrame with an added column `price_with_tax` = `price * (1 + tax_rate)`, computed inside a single `.assign()` call.

```
      price  tax_rate
   +-------+---------+
 0 |  10.0 |    0.05 |
 1 |  20.0 |    0.10 |
 2 |  50.0 |    0.20 |
```

Expected result:

```
      price  tax_rate  price_with_tax
   +-------+---------+---------------+
 0 |  10.0 |    0.05 |         10.50 |
 1 |  20.0 |    0.10 |         22.00 |
 2 |  50.0 |    0.20 |         60.00 |
```

## Hints
1. Use `df.assign(new_col=...)` to add a column without mutating the original DataFrame.
2. Inside `.assign()`, pass a callable (lambda) that receives the intermediate DataFrame so you can reference its columns: `df.assign(price_with_tax=lambda d: d['price'] * (1 + d['tax_rate']))`.
3. The full solution is: `return df.assign(price_with_tax=lambda d: d['price'] * (1 + d['tax_rate']))`.
