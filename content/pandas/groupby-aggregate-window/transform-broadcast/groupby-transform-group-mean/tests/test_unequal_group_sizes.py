def test_unequal_group_sizes():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'category': ['X', 'X', 'X', 'Y'],
        'score': [10, 20, 30, 100]
    })
    result = fn(df)
    import numpy as np
    assert np.isclose(result.loc[result['category'] == 'X', 'group_mean_score'], 20.0).all()
    assert np.isclose(result.loc[result['category'] == 'Y', 'group_mean_score'], 100.0).all()
