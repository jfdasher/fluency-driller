def test_unmatched_row_has_nan_customer_name():
    import pandas as pd
    import numpy as np
    orders = pd.DataFrame({'order_id': [3], 'customer_id': [999], 'amount': [15.0]})
    customers = pd.DataFrame({'customer_id': [101], 'customer_name': ['Alice']})
    result = fn(orders, customers)
    assert result.shape[0] == 1, 'Unmatched order row must be kept'
    assert pd.isna(result.iloc[0]['customer_name']), 'customer_name should be NaN for unmatched row'
