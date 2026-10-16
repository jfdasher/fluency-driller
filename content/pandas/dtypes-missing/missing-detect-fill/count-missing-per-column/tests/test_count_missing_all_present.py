def test_count_missing_all_present():
    import pandas as pd
    from pandas.testing import assert_series_equal
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    expected = pd.Series({'x': 0, 'y': 0}, dtype='int64')
    result = fn(df)
    assert_series_equal(result, expected)
