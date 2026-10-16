def test_exact_equality():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'val': ['3', '7', '1']})
    expected = pd.DataFrame({'val': pd.array([3, 7, 1], dtype='int64')})
    assert_frame_equal(fn(df), expected)
