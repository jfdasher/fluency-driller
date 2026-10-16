def test_bin_age_boundary_35():
    import pandas as pd

    df = pd.DataFrame({'age': [35, 36]})
    result = fn(df)
    # 35 falls in (18, 35] => 'young_adult'; 36 falls in (35, 60] => 'middle_aged'
    assert str(result.loc[0, 'age_group']) == 'young_adult'
    assert str(result.loc[1, 'age_group']) == 'middle_aged'
