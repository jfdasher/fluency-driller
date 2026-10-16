import pandas as pd

def clamp_negatives(s):
    return s.where(s >= 0, other=0)
