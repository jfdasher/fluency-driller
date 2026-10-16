def test_exact_values_and_dtypes():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'dept':   ['HR', 'HR', 'Eng', 'Eng', 'Eng', 'Sales'],
        'salary': [50000, 60000, 90000, 110000, 95000, 45000],
        'years':  [3, 5, 7, 10, 4, 2],
    })
    expected = pd.DataFrame(
        {
            'avg_salary': pd.array([98333.333333, 55000.0, 45000.0], dtype='float64'),
            'max_years':  pd.array([10, 5, 2], dtype='int64'),
            'headcount':  pd.array([3, 2, 1], dtype='int64'),
        },
        index=pd.Index(['Eng', 'HR', 'Sales'], name='dept'),
    )
    result = fn(df)
    assert_frame_equal(result, expected, check_exact=False, rtol=1e-5)
