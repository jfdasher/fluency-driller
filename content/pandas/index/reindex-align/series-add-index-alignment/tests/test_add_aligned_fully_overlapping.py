def test_add_aligned_fully_overlapping():
    import pandas as pd
    from pandas.testing import assert_series_equal
    a = pd.Series([1, 2, 3], index=[10, 20, 30])
    b = pd.Series([4, 5, 6], index=[10, 20, 30])
    expected = pd.Series([5, 7, 9], index=[10, 20, 30])
    result = fn(a, b)
    assert_series_equal(result, expected, check_names=False)
