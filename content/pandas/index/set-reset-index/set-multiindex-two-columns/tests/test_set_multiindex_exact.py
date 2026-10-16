def test_set_multiindex_exact():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'dept': ['eng', 'eng', 'mkt', 'mkt'],
        'emp_id': [101, 102, 201, 202],
        'salary': [90000, 85000, 75000, 80000]
    })
    expected = pd.DataFrame(
        {'salary': [90000, 85000, 75000, 80000]},
        index=pd.MultiIndex.from_tuples(
            [('eng', 101), ('eng', 102), ('mkt', 201), ('mkt', 202)],
            names=['dept', 'emp_id']
        )
    )
    assert_frame_equal(fn(df), expected)
