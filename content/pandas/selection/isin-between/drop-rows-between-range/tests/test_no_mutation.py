def test_no_mutation():
    import pandas as pd
    import types
    fn_src = """
import pandas as pd
def drop_between(df):
    return df[~df['score'].between(40, 70)].reset_index(drop=True)
"""
    mod = types.ModuleType('sol')
    exec(fn_src, mod.__dict__)
    fn = mod.drop_between
    df = pd.DataFrame({'score': [25, 55, 40, 85, 70, 10, 60]})
    original_len = len(df)
    original_values = df['score'].tolist()
    fn(df)
    assert len(df) == original_len
    assert df['score'].tolist() == original_values
