def test_single_month_period_range():
    import pandas as pd
    from pandas.testing import assert_index_equal
    result = fn('2024-03', '2024-03')
    expected = pd.PeriodIndex(['2024-03'], dtype='period[M]')
    assert_index_equal(result, expected)
