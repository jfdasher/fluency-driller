def test_empty_input():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'message': pd.Series([], dtype='object')})
    result = fn(df)
    assert len(result) == 0
    assert list(result.columns) == ['message']
