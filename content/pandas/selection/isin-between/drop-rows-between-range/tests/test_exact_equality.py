def test_exact_equality():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    import importlib, types
    fn_src = """
import pandas as pd
def drop_between(df):
    return df[~df['score'].between(40, 70)].reset_index(drop=True)
"""
    mod = types.ModuleType('sol')
    exec(fn_src, mod.__dict__)
    fn = mod.drop_between
    df = pd.DataFrame({'score': [25, 55, 40, 85, 70, 10, 60]})
    expected = pd.DataFrame({'score': [25, 85, 10]}).reset_index(drop=True)
    result = fn(df)
    assert_frame_equal(result, expected)
