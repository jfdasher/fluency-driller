def test_single_column_frame():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({'x': pd.array([1, 2], dtype='int64')})
    result = fn(df)
    assert result['shape'] == (2, 1)
    assert result['dtypes'] == {'x': np.dtype('int64')}
