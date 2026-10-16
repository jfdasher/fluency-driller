def test_empty_dataframe():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'price': pd.Series([], dtype='float64'), 'tax_rate': pd.Series([], dtype='float64')})
    result = fn(df)
    expected = pd.DataFrame({'price': pd.Series([], dtype='float64'), 'tax_rate': pd.Series([], dtype='float64'), 'price_with_tax': pd.Series([], dtype='float64')})
    assert_frame_equal(result, expected)
