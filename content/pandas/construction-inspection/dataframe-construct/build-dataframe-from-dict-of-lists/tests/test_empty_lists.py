def test_empty_lists():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    result = fn([], [], [])
    expected = pd.DataFrame({'name': pd.Series([], dtype=object),
                             'age':  pd.Series([], dtype=object),
                             'score': pd.Series([], dtype=object)})
    assert result.shape == (0, 3)
    assert list(result.columns) == ['name', 'age', 'score']
