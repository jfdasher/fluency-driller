def test_fully_overlapping_index():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    left = pd.DataFrame({'x': [10, 20]}, index=[0, 1])
    right = pd.DataFrame({'y': [100, 200]}, index=[0, 1])
    result = fn(left, right)
    expected = pd.DataFrame({'x': [10, 20], 'y': [100, 200]}, index=[0, 1])
    assert_frame_equal(result, expected)
