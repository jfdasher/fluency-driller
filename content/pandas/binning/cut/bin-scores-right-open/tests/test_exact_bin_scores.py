def test_exact_bin_scores():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'score': [55, 60, 75, 85, 95, 0]})
    expected = pd.DataFrame({
        'score': [55, 60, 75, 85, 95, 0],
        'grade': pd.Categorical(
            ['F', 'D', 'C', 'B', 'A', 'F'],
            categories=['F', 'D', 'C', 'B', 'A'],
            ordered=True
        )
    })
    assert_frame_equal(fn(df), expected)
