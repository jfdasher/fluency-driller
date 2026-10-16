def test_exact_values_and_dtypes():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'age': [23, 67, 65, 41, 70],
        'status': ['junior', 'junior', 'junior', 'junior', 'junior']
    })
    expected = pd.DataFrame({
        'age': [23, 67, 65, 41, 70],
        'status': ['junior', 'senior', 'senior', 'junior', 'senior']
    })
    assert_frame_equal(fn(df), expected)
