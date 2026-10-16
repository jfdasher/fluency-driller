def test_set_multiindex_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'dept': ['eng', 'eng', 'mkt', 'mkt'],
        'emp_id': [101, 102, 201, 202],
        'salary': [90000, 85000, 75000, 80000]
    })
    original_columns = list(df.columns)
    fn(df)
    assert list(df.columns) == original_columns
    assert isinstance(df.index, pd.RangeIndex)
