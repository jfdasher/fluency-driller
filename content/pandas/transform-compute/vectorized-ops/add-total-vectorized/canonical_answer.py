import pandas as pd


def add_total(df):
    out = df.copy()
    out["total"] = df["a"] + df["b"]
    return out
