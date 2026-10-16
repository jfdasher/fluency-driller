import pandas as pd
import numpy as np

def test_no_mutation():
    df = pd.DataFrame({
        'a': [1.0, 2.0, 3.0, np.nan],
        'b': [np.nan, 5.0, 6.0, np.nan],
        'c': [7.0, 8.0, 9.0, 10.0],
        'd': [np.nan, np.nan, np.nan, np.nan],
    })
    original_columns = list(df.columns)
    fn(df)
    assert list(df.columns) == original_columns
