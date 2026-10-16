def test_fillna_no_nans_in_result():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({'name': ['X', 'Y', 'Z'], 'score': [np.nan, np.nan, 3.0]})
    result = fn(df)
    assert result['score'].isna().sum() == 0, 'no NaNs should remain in score column'
