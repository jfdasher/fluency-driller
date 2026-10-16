def test_fill_score_all_nan():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'name': ['X', 'Y'], 'score': [np.nan, np.nan]})
    expected = pd.DataFrame({'name': ['X', 'Y'], 'score': [0.0, 0.0]})
    assert_frame_equal(fn(df), expected)
