def test_sort_by_score_desc_single_row():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'name': ['Solo'], 'score': [42]})
    expected = pd.DataFrame({'name': ['Solo'], 'score': [42]}, index=[0])
    assert_frame_equal(fn(df), expected)
