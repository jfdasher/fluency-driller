def test_exact_monthly_period_range():
    import pandas as pd
    from pandas.testing import assert_index_equal
    expected = pd.PeriodIndex(['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06'], dtype='period[M]')
    result = fn('2023-01', '2023-06')
    assert_index_equal(result, expected)
