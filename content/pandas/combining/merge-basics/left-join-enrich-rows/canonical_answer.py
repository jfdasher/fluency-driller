import pandas as pd

def enrich_orders(orders, customers):
    result = orders.merge(customers, on='customer_id', how='left')
    return result[['order_id', 'customer_id', 'amount', 'customer_name']]
