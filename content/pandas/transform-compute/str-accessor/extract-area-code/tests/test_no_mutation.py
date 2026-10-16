import pandas as pd

def test_no_mutation():
    df = pd.DataFrame({'phone': ['(212) 555-1234', '(415) 867-5309']})
    original_columns = list(df.columns)
    original_values = df['phone'].tolist()
    fn(df)
    assert list(df.columns) == original_columns
    assert df['phone'].tolist() == original_values
