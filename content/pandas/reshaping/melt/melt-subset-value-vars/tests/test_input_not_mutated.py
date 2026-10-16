def test_input_not_mutated():
    import pandas as pd
    df = pd.DataFrame({
        'id': [1, 2],
        'name': ['Ada', 'Bob'],
        'q1': [10, 40],
        'q2': [20, 50],
        'q3': [30, 60]
    })
    original_cols = list(df.columns)
    original_shape = df.shape
    fn(df)
    assert list(df.columns) == original_cols
    assert df.shape == original_shape
