def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'score': [55, 60, 75, 85, 95, 0]})
    _ = fn(df)
    assert 'grade' not in df.columns
