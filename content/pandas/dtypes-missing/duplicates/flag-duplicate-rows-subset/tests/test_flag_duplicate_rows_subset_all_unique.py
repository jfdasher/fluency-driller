def test_flag_duplicate_rows_subset_all_unique():
    import pandas as pd
    from pandas.testing import assert_series_equal
    df = pd.DataFrame({
        'name':   ['Alice', 'Bob', 'Carol'],
        'dept':   ['Eng',   'Mkt', 'HR'],
        'salary': [90000,   70000, 80000]
    })
    expected = pd.Series([False, False, False], name='is_dup', dtype=bool)
    assert_series_equal(fn(df), expected)
