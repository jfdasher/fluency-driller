import pandas as pd

def stack_frames(top, bottom):
    return pd.concat([top, bottom], ignore_index=True)
