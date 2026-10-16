def test_single_group():
    import pandas as pd
    from pandas.testing import assert_series_equal
    df = pd.DataFrame({'dept': ['X','X','X'], 'score': [1,2,3]})
    expected = pd.Series([3], index=pd.Index(['X'], name='dept'))
    assert_series_equal(fn(df), expected)
