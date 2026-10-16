def test_bin_age_exact():
    import pandas as pd
    from pandas.testing import assert_frame_equal

    df = pd.DataFrame({'age': [5, 22, 45, 70, 18]})

    expected = pd.DataFrame({
        'age': [5, 22, 45, 70, 18],
        'age_group': pd.Categorical(
            ['youth', 'young_adult', 'middle_aged', 'senior', 'youth'],
            categories=['youth', 'young_adult', 'middle_aged', 'senior'],
            ordered=True
        )
    })

    assert_frame_equal(fn(df), expected)
