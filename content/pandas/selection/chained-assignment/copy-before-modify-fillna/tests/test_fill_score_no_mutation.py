def test_fill_score_no_mutation():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({'name': ['Alice', 'Bob'], 'score': [np.nan, 55.0]})
    original_score = df['score'].copy()
    fn(df)
    import pandas.testing as tm
    tm.assert_series_equal(df['score'], original_score)
