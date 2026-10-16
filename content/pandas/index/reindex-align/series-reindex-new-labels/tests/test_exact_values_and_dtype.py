def test_exact_values_and_dtype():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_series_equal
    s = pd.Series([10.0, 20.0, 30.0], index=['alpha', 'beta', 'gamma'], name='value')
    new_index = ['alpha', 'gamma', 'delta', 'epsilon']
    expected = pd.Series([10.0, 30.0, np.nan, np.nan], index=['alpha', 'gamma', 'delta', 'epsilon'], name='value')
    assert_series_equal(fn(s, new_index), expected)
