def test_flag_duplicate_rows_subset_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'name':   ['Alice', 'Bob', 'Alice'],
        'dept':   ['Eng',   'Mkt', 'Eng'],
        'salary': [90000,   70000, 95000]
    })
    original_columns = list(df.columns)
    original_values = df.copy()
    _ = fn(df)
    assert list(df.columns) == original_columns
    import pandas.testing as pdt
    pdt.assert_frame_equal(df, original_values)
