def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'color': ['red', 'blue', 'red', 'green', 'blue', 'red']})
    original_columns = list(df.columns)
    original_values = df['color'].tolist()
    fn(df)
    assert list(df.columns) == original_columns
    assert df['color'].tolist() == original_values
