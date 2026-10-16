def test_uppercase_name_empty():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'name': pd.Series([], dtype='object'), 'score': pd.Series([], dtype='int64')})
    expected = pd.DataFrame({'name': pd.Series([], dtype='object'), 'score': pd.Series([], dtype='int64')})
    result = fn(df)
    assert_frame_equal(result, expected)
    assert len(result) == 0
