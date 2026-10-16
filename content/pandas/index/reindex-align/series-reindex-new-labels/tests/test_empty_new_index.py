def test_empty_new_index():
    import pandas as pd
    from pandas.testing import assert_series_equal
    s = pd.Series([10.0, 20.0], index=['a', 'b'], name='val')
    new_index = []
    expected = pd.Series([], index=pd.Index([]), dtype='float64', name='val')
    assert_series_equal(fn(s, new_index), expected)
