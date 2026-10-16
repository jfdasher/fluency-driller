def test_count_missing_exact():
    import pandas as pd
    from pandas.testing import assert_series_equal
    import numpy as np
    df = pd.DataFrame({
        'age': [np.nan, 25.0, 30.0, np.nan],
        'score': [8.5, np.nan, 7.0, np.nan],
        'name': ['Alice', 'Bob', None, 'Dana']
    })
    expected = pd.Series({'age': 2, 'score': 2, 'name': 1}, dtype='int64')
    result = fn(df)
    assert_series_equal(result, expected)
