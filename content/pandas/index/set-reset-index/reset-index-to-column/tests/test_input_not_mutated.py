def test_input_not_mutated():
    import pandas as pd
    df = pd.DataFrame(
        {'score': [85, 92, 78]},
        index=pd.Index(['Alice', 'Bob', 'Carol'], name='name')
    )
    original_index_name = df.index.name
    original_columns = list(df.columns)
    _ = fn(df)
    assert df.index.name == original_index_name
    assert list(df.columns) == original_columns
