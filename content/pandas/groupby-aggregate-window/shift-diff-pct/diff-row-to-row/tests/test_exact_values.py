def test_exact_values():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'price': [10.0, 15.0, 13.0, 20.0, 18.0]})
    expected = pd.DataFrame({
        'price': [10.0, 15.0, 13.0, 20.0, 18.0],
        'delta': [np.nan, 5.0, -2.0, 7.0, -2.0]
    })
    assert_frame_equal(fn(df), expected)
