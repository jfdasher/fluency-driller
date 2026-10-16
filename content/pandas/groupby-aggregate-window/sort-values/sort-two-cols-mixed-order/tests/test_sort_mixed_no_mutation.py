def test_sort_mixed_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'dept': ['HR', 'IT', 'HR', 'IT', 'OPS'],
        'salary': [50000, 90000, 70000, 80000, 60000]
    })
    original_index = list(df.index)
    original_dept = list(df['dept'])
    fn(df)
    assert list(df.index) == original_index
    assert list(df['dept']) == original_dept
