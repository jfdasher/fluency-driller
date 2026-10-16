def test_exact_index_name_and_data():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'score': [88, 95, 72], 'grade': ['B', 'A', 'C']})
    expected = pd.DataFrame(
        {'score': [88, 95, 72], 'grade': ['B', 'A', 'C']},
        index=pd.Index([0, 1, 2], name='student_id')
    )
    assert_frame_equal(fn(df), expected)
