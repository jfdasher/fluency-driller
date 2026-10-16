def test_clamp_negatives_exact():
    import pandas as pd
    from pandas.testing import assert_series_equal
    s = pd.Series([3, -1, 7, -4, 0], dtype='int64')
    expected = pd.Series([3, 0, 7, 0, 0], dtype='int64')
    assert_series_equal(fn(s), expected)
