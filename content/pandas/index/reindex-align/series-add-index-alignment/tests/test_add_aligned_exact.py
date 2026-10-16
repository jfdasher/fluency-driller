def test_add_aligned_exact():
    import pandas as pd
    from pandas.testing import assert_series_equal
    a = pd.Series([10, 20, 30], index=[1, 2, 3])
    b = pd.Series([200, 300, 400], index=[2, 3, 4])
    expected = pd.Series([float('nan'), 220.0, 330.0, float('nan')], index=[1, 2, 3, 4])
    result = fn(a, b)
    assert_series_equal(result, expected, check_names=False)
