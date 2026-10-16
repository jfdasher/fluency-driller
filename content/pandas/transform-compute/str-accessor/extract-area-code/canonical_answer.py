import pandas as pd

def extract_area_code(df):
    return df['phone'].str.extract(r'\((?P<area_code>\d{3})\)')
