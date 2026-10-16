def test_boundary_inclusive():
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
    df = pd.DataFrame({'score': [40, 70, 39, 71]})
    result = fn(df)
    assert set(result['score'].tolist()) == {39, 71}
