import pandas as pd

def build_df(data):
    return pd.DataFrame(data, index=['c', 'a', 'b'], columns=['score', 'name'])
