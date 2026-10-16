def test_exact_counts():
    import pandas as pd
    from pandas.testing import assert_series_equal
    df = pd.DataFrame({'dept': ['A','B','A','C','B','B'], 'score': [10,20,30,40,50,60]})
    expected = pd.Series([2, 3, 1], index=pd.Index(['A','B','C'], name='dept'))
    assert_series_equal(fn(df), expected)
