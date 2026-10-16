def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'age': pd.array([25, 30, 22], dtype='int64'),
        'score': pd.array([88.5, 92.0, 79.3], dtype='float64'),
        'name': ['Alice', 'Bob', 'Carol']
    })
    original_columns = list(df.columns)
    original_shape = df.shape
    fn(df)
    assert list(df.columns) == original_columns
    assert df.shape == original_shape
