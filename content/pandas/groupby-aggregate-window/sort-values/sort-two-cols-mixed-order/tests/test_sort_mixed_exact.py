def test_sort_mixed_exact():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'dept': ['HR', 'IT', 'HR', 'IT', 'OPS'],
        'salary': [50000, 90000, 70000, 80000, 60000]
    })
    expected = pd.DataFrame({
        'dept': ['HR', 'HR', 'IT', 'IT', 'OPS'],
        'salary': [70000, 50000, 90000, 80000, 60000]
    }, index=[2, 0, 1, 3, 4])
    assert_frame_equal(fn(df), expected)
