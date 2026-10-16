---
kind: idiom
status: approved
topic: combining/merge-basics
entry_point: enrich_orders
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: left-join to enrich rows while keeping every left row (how='left')
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `orders` and `customers`, left-join `orders` to `customers` on `customer_id` to enrich each order row with `customer_name`, keeping every order row even if no matching customer exists.

`orders`:

     order_id  customer_id  amount
   +----------+------------+-------+
 0 |        1 |        101 |  25.0 |
 1 |        2 |        102 |  80.0 |
 2 |        3 |        999 |  15.0 |

`customers`:

     customer_id  customer_name
   +------------+--------------+
 0 |        101 |       Alice  |
 1 |        102 |       Bob    |

Return a new DataFrame with columns `order_id`, `customer_id`, `amount`, `customer_name` (in that order); unmatched rows get `NaN` for `customer_name`.

## Hints
1. Use `pd.DataFrame.merge()` with `on='customer_id'`.
2. Pass `how='left'` to keep every row from the left (orders) DataFrame regardless of a match.
3. After merging, select and reorder columns: `result[['order_id', 'customer_id', 'amount', 'customer_name']]`.
