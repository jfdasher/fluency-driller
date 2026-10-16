def test_empty_frames():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    top = pd.DataFrame({'name': pd.Series([], dtype='object'), 'score': pd.Series([], dtype='int64')})
    bottom = pd.DataFrame({'name': pd.Series([], dtype='object'), 'score': pd.Series([], dtype='int64')})
    result = fn(top, bottom)
    expected = pd.DataFrame({'name': pd.Series([], dtype='object'), 'score': pd.Series([], dtype='int64')})
    assert_frame_equal(result, expected)
    assert list(result.index) == []
