import pandas as pd


def test_case_1():
    df = pd.DataFrame({"a": [5], "b": [7]})
    _ = fn(df)
    # input must not be mutated
    assert list(df.columns) == ["a", "b"]
