def test_input_not_mutated():
    import pandas as pd
    from pandas.testing import assert_series_equal
    s = pd.Series([10.0, 20.0, 30.0], index=['alpha', 'beta', 'gamma'], name='value')
    s_original = s.copy()
    new_index = ['alpha', 'gamma', 'delta', 'epsilon']
    fn(s, new_index)
    assert_series_equal(s, s_original)
