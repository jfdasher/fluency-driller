def test_fillna_no_mutation():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({'name': ['Alice', 'Bob'], 'score': [np.nan, 5.0]})
    _ = fn(df)
    assert pd.isna(df.loc[0, 'score']), 'original df must not be mutated'
