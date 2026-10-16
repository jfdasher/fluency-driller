def test_demean_exact():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'group': ['A', 'B', 'A', 'B', 'A'], 'value': [10, 20, 30, 40, 50]})
    expected = pd.DataFrame({'value_demeaned': pd.Series([-20.0, -10.0, 0.0, 10.0, 20.0])})
    assert_frame_equal(fn(df), expected)
