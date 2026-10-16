def test_no_mutation_of_input():
    import pandas as pd
    df = pd.DataFrame({
        'dept':   ['HR', 'HR', 'Eng'],
        'salary': [50000, 60000, 90000],
        'years':  [3, 5, 7],
    })
    original_cols = list(df.columns)
    original_shape = df.shape
    fn(df)
    assert list(df.columns) == original_cols
    assert df.shape == original_shape
