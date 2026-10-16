def test_sort_by_score_desc_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Carol'],
        'score': [82, 95, 70]
    })
    original_index = df.index.tolist()
    original_scores = df['score'].tolist()
    fn(df)
    assert df.index.tolist() == original_index
    assert df['score'].tolist() == original_scores
