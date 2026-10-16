def test_ids_in_both_exact():
    import pandas as pd
    from pandas.testing import assert_series_equal
    left = pd.DataFrame({'id': [1, 2, 3], 'val_l': ['a', 'b', 'c']})
    right = pd.DataFrame({'id': [1, 3, 5], 'val_r': ['x', 'y', 'z']})
    result = fn(left, right)
    expected = pd.Series([1, 3], name='id', dtype='int64')
    assert_series_equal(result, expected)
