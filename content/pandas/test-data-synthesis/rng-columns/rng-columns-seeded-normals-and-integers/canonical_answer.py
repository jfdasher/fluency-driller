import pandas as pd
import numpy as np

def build_rng_df():
    rng = np.random.default_rng(seed=42)
    scores = rng.standard_normal(5)
    counts = rng.integers(0, 10, size=5)
    return pd.DataFrame({'score': scores, 'count': counts})
