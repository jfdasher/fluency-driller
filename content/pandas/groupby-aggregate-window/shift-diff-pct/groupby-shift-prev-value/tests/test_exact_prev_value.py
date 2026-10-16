def test_exact_prev_value():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'group': ['A', 'A', 'A', 'B', 'B'],
        'value': [10, 20, 30, 100, 200]
    })
    expected = pd.DataFrame({
        'group': ['A', 'A', 'A', 'B', 'B'],
        'value': [10, 20, 30, 100, 200],
        'prev_value': [np.nan, 10.0, 20.0, np.nan, 100.0]
    })
    assert_frame_equal(fn(df), expected)
