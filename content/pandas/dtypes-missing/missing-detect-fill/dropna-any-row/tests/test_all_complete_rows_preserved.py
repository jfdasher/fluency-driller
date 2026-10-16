def test_all_complete_rows_preserved():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'x': [1.0, 2.0, 3.0], 'y': [4.0, 5.0, 6.0]})
    result = fn(df)
    assert_frame_equal(result, df)
