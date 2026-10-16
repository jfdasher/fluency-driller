def test_input_not_mutated():
    import pandas as pd
    orders = pd.DataFrame({'order_id': [1, 2], 'customer_id': [101, 102], 'amount': [25.0, 80.0]})
    customers = pd.DataFrame({'customer_id': [101, 102], 'customer_name': ['Alice', 'Bob']})
    orders_cols_before = list(orders.columns)
    customers_cols_before = list(customers.columns)
    fn(orders, customers)
    assert list(orders.columns) == orders_cols_before, 'orders must not be mutated'
    assert list(customers.columns) == customers_cols_before, 'customers must not be mutated'
