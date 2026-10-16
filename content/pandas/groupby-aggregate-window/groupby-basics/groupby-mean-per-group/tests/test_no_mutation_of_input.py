def test_no_mutation_of_input():
    import pandas as pd
    df = pd.DataFrame({'team': ['A', 'B', 'A', 'B', 'A'], 'score': [10, 20, 30, 40, 20]})
    original_columns = list(df.columns)
    original_shape = df.shape
    fn(df)
    assert list(df.columns) == original_columns
    assert df.shape == original_shape
