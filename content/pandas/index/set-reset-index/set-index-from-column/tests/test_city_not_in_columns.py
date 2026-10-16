def test_city_not_in_columns():
    import pandas as pd
    df = pd.DataFrame({
        'city': ['NYC', 'LA', 'CHI'],
        'population': [8336817, 3979576, 2693976],
        'area': [302, 469, 227]
    })
    result = fn(df)
    assert 'city' not in result.columns, "'city' should not remain as a column"
    assert result.index.name == 'city', "index name should be 'city'"
