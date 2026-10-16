def test_flag_duplicate_rows_subset_exact():
    import pandas as pd
    from pandas.testing import assert_series_equal
    df = pd.DataFrame({
        'name':   ['Alice', 'Bob', 'Alice', 'Carol', 'Bob',   'Alice'],
        'dept':   ['Eng',   'Mkt', 'Eng',   'Eng',   'Mkt',   'HR'],
        'salary': [90000,   70000, 95000,   80000,   72000,   88000]
    })
    expected = pd.Series([False, False, True, False, True, False], name='is_dup', dtype=bool)
    assert_series_equal(fn(df), expected)
