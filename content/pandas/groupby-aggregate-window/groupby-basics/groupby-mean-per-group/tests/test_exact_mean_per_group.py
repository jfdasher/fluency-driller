def test_exact_mean_per_group():
    import pandas as pd
    from pandas.testing import assert_series_equal
    df = pd.DataFrame({'team': ['A', 'B', 'A', 'B', 'A'], 'score': [10, 20, 30, 40, 20]})
    expected = pd.Series([20.0, 30.0], index=pd.Index(['A', 'B'], name='team'), name='score')
    assert_series_equal(fn(df), expected)
