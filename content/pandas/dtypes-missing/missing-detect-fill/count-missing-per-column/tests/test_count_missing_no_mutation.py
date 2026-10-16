def test_count_missing_no_mutation():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({
        'age': [np.nan, 25.0, 30.0, np.nan],
        'score': [8.5, np.nan, 7.0, np.nan],
        'name': ['Alice', 'Bob', None, 'Dana']
    })
    original_values = df.copy()
    fn(df)
    from pandas.testing import assert_frame_equal
    assert_frame_equal(df, original_values)
