def test_exact_equality():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'city': ['NYC', 'LA', 'CHI'],
        'population': [8336817, 3979576, 2693976],
        'area': [302, 469, 227]
    })
    expected = pd.DataFrame(
        {'population': [8336817, 3979576, 2693976], 'area': [302, 469, 227]},
        index=pd.Index(['NYC', 'LA', 'CHI'], name='city')
    )
    assert_frame_equal(fn(df), expected)
