def test_no_mutation_of_input():
    import pandas as pd
    df = pd.DataFrame({'score': [95, 82, 67, 55, 90]})
    original_cols = list(df.columns)
    fn(df)
    assert list(df.columns) == original_cols, 'input df should not gain a grade column'
