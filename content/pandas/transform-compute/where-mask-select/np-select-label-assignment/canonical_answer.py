import pandas as pd
import numpy as np

def assign_grade(df):
    conditions = [
        df['score'] >= 90,
        df['score'] >= 75,
        df['score'] >= 60,
    ]
    choices = ['A', 'B', 'C']
    out = df.copy()
    out['grade'] = np.select(conditions, choices, default='F')
    return out
