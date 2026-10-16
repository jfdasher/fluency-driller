def test_single_group():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'dept':   ['HR', 'HR'],
        'salary': [40000, 60000],
        'years':  [2, 8],
    })
    result = fn(df)
    assert result.index.name == 'dept'
    assert list(result.columns) == ['avg_salary', 'max_years', 'headcount']
    assert result.loc['HR', 'avg_salary'] == 50000.0
    assert result.loc['HR', 'max_years'] == 8
    assert result.loc['HR', 'headcount'] == 2
