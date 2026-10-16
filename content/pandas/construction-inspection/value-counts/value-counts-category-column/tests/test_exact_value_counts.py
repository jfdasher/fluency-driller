def test_exact_value_counts():
    import pandas as pd
    from pandas.testing import assert_series_equal
    df = pd.DataFrame({'color': ['red', 'blue', 'red', 'green', 'blue', 'red']})
    expected = pd.Series(
        [3, 2, 1],
        index=pd.Index(['red', 'blue', 'green'], name='color'),
        name='count',
        dtype='int64'
    )
    assert_series_equal(fn(df), expected)
