def test_fillna_exact():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'name': ['Alice', 'Bob', 'Carol', 'David'], 'score': [np.nan, 8.5, np.nan, 7.0]})
    expected = pd.DataFrame({'name': ['Alice', 'Bob', 'Carol', 'David'], 'score': [0.0, 8.5, 0.0, 7.0]})
    assert_frame_equal(fn(df), expected)
