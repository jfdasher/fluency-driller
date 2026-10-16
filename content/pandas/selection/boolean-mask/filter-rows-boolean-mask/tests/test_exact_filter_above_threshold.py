def test_exact_filter_above_threshold():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'name': ['Alice', 'Bob', 'Carol', 'Dave'], 'score': [82, 55, 91, 70]})
    expected = pd.DataFrame({'name': ['Alice', 'Carol'], 'score': [82, 91]}, index=[0, 1])
    expected['score'] = expected['score'].astype('int64')
    result = fn(df, 70)
    assert_frame_equal(result, expected)
