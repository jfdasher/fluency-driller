def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'city': ['NYC', 'LA', 'CHI'],
        'population': [8336817, 3979576, 2693976],
        'area': [302, 469, 227]
    })
    original_columns = list(df.columns)
    fn(df)
    assert list(df.columns) == original_columns, 'Input df was mutated'
