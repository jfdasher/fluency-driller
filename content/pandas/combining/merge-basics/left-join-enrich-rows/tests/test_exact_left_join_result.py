def test_exact_left_join_result():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    orders = pd.DataFrame({'order_id': [1, 2, 3], 'customer_id': [101, 102, 999], 'amount': [25.0, 80.0, 15.0]})
    customers = pd.DataFrame({'customer_id': [101, 102], 'customer_name': ['Alice', 'Bob']})
    expected = pd.DataFrame({
        'order_id': pd.array([1, 2, 3], dtype='int64'),
        'customer_id': pd.array([101, 102, 999], dtype='int64'),
        'amount': pd.array([25.0, 80.0, 15.0], dtype='float64'),
        'customer_name': pd.array(['Alice', 'Bob', np.nan], dtype='object')
    })
    assert_frame_equal(fn(orders, customers).reset_index(drop=True), expected)
