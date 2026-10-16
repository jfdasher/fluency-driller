def test_period_range_dtype_and_length():
    import pandas as pd
    result = fn('2020-01', '2020-12')
    assert len(result) == 12
    assert result.dtype == 'period[M]'
    assert result[0] == pd.Period('2020-01', freq='M')
    assert result[-1] == pd.Period('2020-12', freq='M')
