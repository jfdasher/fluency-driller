def test_single_category():
    import pandas as pd
    from pandas.testing import assert_series_equal
    df = pd.DataFrame({'color': ['blue', 'blue', 'blue']})
    expected = pd.Series(
        [3],
        index=pd.Index(['blue'], name='color'),
        name='count',
        dtype='int64'
    )
    assert_series_equal(fn(df), expected)
