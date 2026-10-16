def test_no_mutation_of_input():
    import pandas as pd
    df = pd.DataFrame({'value': [10, 20, 30, 40, 50]}, index=list('abcde'))
    original_index = df.index.tolist()
    original_values = df['value'].tolist()
    fn(df)
    assert df.index.tolist() == original_index
    assert df['value'].tolist() == original_values
