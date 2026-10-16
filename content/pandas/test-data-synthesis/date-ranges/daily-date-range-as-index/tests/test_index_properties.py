def test_index_properties():
    import pandas as pd

    result = fn('2023-06-15', 5)

    assert isinstance(result.index, pd.DatetimeIndex)
    assert result.index.name == 'date'
    assert result.index.freq == 'D' or str(result.index.freq) == 'D'
    assert len(result) == 5
    assert result.index[0] == pd.Timestamp('2023-06-15')
    assert result.index[-1] == pd.Timestamp('2023-06-19')
