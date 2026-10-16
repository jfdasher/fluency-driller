def test_no_mutation_of_input():
    import pandas as pd
    df = pd.DataFrame({
        'category': ['A', 'B', 'A', 'B', 'A'],
        'score': [10, 20, 30, 40, 50]
    })
    original_cols = list(df.columns)
    fn(df)
    assert list(df.columns) == original_cols, 'Input df must not be mutated'
