def test_single_row():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'val': ['42']})
    result = fn(df)
    expected = pd.DataFrame({'val': pd.array([42], dtype='int64')})
    assert_frame_equal(result, expected)
