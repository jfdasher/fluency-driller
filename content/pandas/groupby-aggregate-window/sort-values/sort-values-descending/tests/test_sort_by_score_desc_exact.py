def test_sort_by_score_desc_exact():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Carol', 'David', 'Eve'],
        'score': [82, 95, 70, 95, 88]
    })
    expected = pd.DataFrame({
        'name': ['Bob', 'David', 'Eve', 'Alice', 'Carol'],
        'score': [95, 95, 88, 82, 70]
    }, index=[1, 3, 4, 0, 2])
    assert_frame_equal(fn(df), expected)
