def test_no_mutation_of_input():
    import pandas as pd
    df = pd.DataFrame({'price': [10.0, 20.0], 'tax_rate': [0.05, 0.10]})
    original_columns = list(df.columns)
    fn(df)
    assert list(df.columns) == original_columns, 'input df should not be mutated'
