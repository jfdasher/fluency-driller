def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'dept': ['A','B','A','C','B','B'], 'score': [10,20,30,40,50,60]})
    original_cols = list(df.columns)
    original_shape = df.shape
    fn(df)
    assert list(df.columns) == original_cols
    assert df.shape == original_shape
