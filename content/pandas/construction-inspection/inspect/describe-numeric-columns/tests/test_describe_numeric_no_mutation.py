def test_describe_numeric_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'score': [85.0, 92.0, 78.0, 95.0], 'attempts': [3, 1, 4, 2]})
    original_shape = df.shape
    original_columns = list(df.columns)
    fn(df)
    assert df.shape == original_shape
    assert list(df.columns) == original_columns
