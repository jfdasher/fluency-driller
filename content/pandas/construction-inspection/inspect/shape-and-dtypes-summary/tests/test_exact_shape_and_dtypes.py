def test_exact_shape_and_dtypes():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({
        'age': pd.array([25, 30, 22], dtype='int64'),
        'score': pd.array([88.5, 92.0, 79.3], dtype='float64'),
        'name': ['Alice', 'Bob', 'Carol']
    })
    result = fn(df)
    assert result['shape'] == (3, 3)
    expected_dtypes = dict(df.dtypes)
    assert result['dtypes'] == expected_dtypes
    assert result['dtypes']['age'] == np.dtype('int64')
    assert result['dtypes']['score'] == np.dtype('float64')
    assert result['dtypes']['name'] == np.dtype('O')
