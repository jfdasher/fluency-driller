def test_single_row_gives_nan_delta():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'price': [42.0]})
    result = fn(df)
    expected = pd.DataFrame({'price': [42.0], 'delta': [np.nan]})
    assert_frame_equal(result, expected)
