import pandas as pd

def name_row_index(df):
    out = df.copy()
    out.index.name = "student_id"
    return out
