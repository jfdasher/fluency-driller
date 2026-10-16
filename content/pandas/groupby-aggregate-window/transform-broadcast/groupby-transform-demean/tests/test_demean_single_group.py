def test_demean_single_group():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'group': ['X', 'X', 'X'], 'value': [5, 10, 15]})
    expected = pd.DataFrame({'value_demeaned': pd.Series([-5.0, 0.0, 5.0])})
    assert_frame_equal(fn(df), expected)
