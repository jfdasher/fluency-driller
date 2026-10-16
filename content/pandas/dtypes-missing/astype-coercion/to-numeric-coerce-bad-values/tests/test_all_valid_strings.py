def test_all_valid_strings():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'value': ['10', '20', '30']})
    result = fn(df)
    expected = pd.DataFrame({'value': pd.to_numeric(pd.Series(['10', '20', '30']), errors='coerce')})
    assert_frame_equal(result, expected, check_dtype=False)
    assert result['value'].tolist() == [10, 20, 30]
