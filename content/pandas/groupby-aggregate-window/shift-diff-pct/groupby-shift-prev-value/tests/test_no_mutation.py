def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'group': ['A', 'A', 'B', 'B'],
        'value': [1, 2, 3, 4]
    })
    original_cols = list(df.columns)
    fn(df)
    assert list(df.columns) == original_cols, 'input df should not be mutated'
