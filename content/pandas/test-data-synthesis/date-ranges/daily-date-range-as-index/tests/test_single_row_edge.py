def test_single_row_edge():
    import pandas as pd
    from pandas.testing import assert_frame_equal

    result = fn('2020-03-01', 1)

    idx = pd.date_range(start='2020-03-01', periods=1, freq='D', name='date')
    expected = pd.DataFrame({'value': [0]}, index=idx)

    assert_frame_equal(result, expected)
