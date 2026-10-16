def test_loc_iloc_exact_values():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'value': [10, 20, 30, 40, 50]}, index=list('abcde'))
    loc_res, iloc_res = fn(df)
    expected_loc = pd.DataFrame({'value': [20, 30, 40]}, index=list('bcd'))
    expected_iloc = pd.DataFrame({'value': [10, 20]}, index=list('ab'))
    assert_frame_equal(loc_res, expected_loc)
    assert_frame_equal(iloc_res, expected_iloc)
