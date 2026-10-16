def test_exact_grade_assignment():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'score': [95, 82, 67, 55, 90]})
    expected = pd.DataFrame({
        'score': [95, 82, 67, 55, 90],
        'grade': pd.array(['A', 'B', 'C', 'F', 'A'], dtype=object)
    })
    assert_frame_equal(fn(df), expected)
