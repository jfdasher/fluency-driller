import pandas as pd

def build_dataframe(names, ages, scores):
    return pd.DataFrame({'name': names, 'age': ages, 'score': scores})
