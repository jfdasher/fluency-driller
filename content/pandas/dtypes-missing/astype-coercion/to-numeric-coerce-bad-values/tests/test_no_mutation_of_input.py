def test_no_mutation_of_input():
    import pandas as pd
    df = pd.DataFrame({'value': ['3', 'abc', '7', '?', '1.5']})
    original_values = df['value'].tolist()
    fn(df)
    assert df['value'].tolist() == original_values, 'input df was mutated'
