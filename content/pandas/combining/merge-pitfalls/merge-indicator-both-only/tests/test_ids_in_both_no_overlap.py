def test_ids_in_both_no_overlap():
    import pandas as pd
    from pandas.testing import assert_series_equal
    left = pd.DataFrame({'id': [1, 2], 'val_l': ['a', 'b']})
    right = pd.DataFrame({'id': [3, 4], 'val_r': ['x', 'y']})
    result = fn(left, right)
    expected = pd.Series([], name='id', dtype='int64')
    assert_series_equal(result, expected)
