def test_exact_values_and_dtypes():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    names  = ['Alice', 'Bob', 'Charlie']
    ages   = [25, 30, 35]
    scores = [88.5, 92.0, 79.3]
    result = fn(names, ages, scores)
    expected = pd.DataFrame(
        {'name': pd.Series(['Alice', 'Bob', 'Charlie'], dtype=object),
         'age':  pd.Series([25, 30, 35], dtype='int64'),
         'score': pd.Series([88.5, 92.0, 79.3], dtype='float64')}
    )
    assert_frame_equal(result, expected)
