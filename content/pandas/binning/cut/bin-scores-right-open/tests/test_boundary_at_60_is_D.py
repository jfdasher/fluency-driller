def test_boundary_at_60_is_D():
    import pandas as pd
    df = pd.DataFrame({'score': [59, 60]})
    result = fn(df)
    assert str(result.loc[0, 'grade']) == 'F'
    assert str(result.loc[1, 'grade']) == 'D'
