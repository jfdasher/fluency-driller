def test_single_group():
    import pandas as pd
    from pandas.testing import assert_series_equal
    df = pd.DataFrame({'team': ['X', 'X', 'X'], 'score': [5, 15, 25]})
    expected = pd.Series([15.0], index=pd.Index(['X'], name='team'), name='score')
    assert_series_equal(fn(df), expected)
