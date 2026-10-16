def test_single_row_group():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({
        'group': ['X', 'Y', 'Y'],
        'value': [5, 10, 15]
    })
    result = fn(df)
    import math
    assert math.isnan(result.loc[0, 'prev_value']), 'single-member group first row should be NaN'
    assert math.isnan(result.loc[1, 'prev_value']), 'first row of Y group should be NaN'
    assert result.loc[2, 'prev_value'] == 10.0
