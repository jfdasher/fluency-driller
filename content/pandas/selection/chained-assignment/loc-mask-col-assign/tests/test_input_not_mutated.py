def test_input_not_mutated():
    import pandas as pd
    df = pd.DataFrame({
        'age': [23, 67, 65, 41, 70],
        'status': ['junior', 'junior', 'junior', 'junior', 'junior']
    })
    original_status = df['status'].tolist()
    fn(df)
    assert df['status'].tolist() == original_status
