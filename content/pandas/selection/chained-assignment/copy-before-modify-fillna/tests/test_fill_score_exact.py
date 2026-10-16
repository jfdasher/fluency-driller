def test_fill_score_exact():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'name': ['Alice', 'Bob', 'Carol', 'Dave'], 'score': [np.nan, 88.0, np.nan, 95.0]})
    expected = pd.DataFrame({'name': ['Alice', 'Bob', 'Carol', 'Dave'], 'score': [0.0, 88.0, 0.0, 95.0]})
    assert_frame_equal(fn(df), expected)
