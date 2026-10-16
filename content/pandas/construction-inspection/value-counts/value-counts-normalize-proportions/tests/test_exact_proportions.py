def test_exact_proportions():
    import pandas as pd
    from pandas.testing import assert_series_equal
    s = pd.Series(['cat', 'dog', 'cat', 'cat', 'dog'])
    expected = pd.Series({'cat': 0.6, 'dog': 0.4}, dtype='float64')
    expected.index.name = None
    expected.name = None
    result = fn(s)
    assert_series_equal(result, expected)
