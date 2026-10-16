import pandas as pd

def test_result_dtype_is_object():
    df = pd.DataFrame({'phone': ['(800) 123-4567']})
    result = fn(df)
    assert result['area_code'].dtype == object
    assert result['area_code'].iloc[0] == '800'
