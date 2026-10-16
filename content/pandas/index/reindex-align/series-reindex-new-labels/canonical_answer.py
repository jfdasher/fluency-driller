import pandas as pd

def reindex_series(s, new_index):
    return s.reindex(new_index)
