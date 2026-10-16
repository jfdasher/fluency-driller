def test_empty_list_returns_empty_dataframe():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    result = fn([])
    expected = pd.DataFrame()
    assert_frame_equal(result, expected)
