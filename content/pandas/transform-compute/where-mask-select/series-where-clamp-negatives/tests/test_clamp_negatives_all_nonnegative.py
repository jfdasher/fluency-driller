def test_clamp_negatives_all_nonnegative():
    import pandas as pd
    from pandas.testing import assert_series_equal
    s = pd.Series([0, 5, 10], dtype='int64')
    expected = pd.Series([0, 5, 10], dtype='int64')
    assert_series_equal(fn(s), expected)
