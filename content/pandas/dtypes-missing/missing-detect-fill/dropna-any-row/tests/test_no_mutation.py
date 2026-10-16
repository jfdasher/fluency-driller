def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'a': [1.0, float('nan'), 7.0],
        'b': [2.0, 5.0, float('nan')],
    })
    original_shape = df.shape
    original_na_count = df.isna().sum().sum()
    fn(df)
    assert df.shape == original_shape
    assert df.isna().sum().sum() == original_na_count
