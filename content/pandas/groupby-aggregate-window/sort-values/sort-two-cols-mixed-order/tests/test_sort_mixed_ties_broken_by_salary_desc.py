def test_sort_mixed_ties_broken_by_salary_desc():
    import pandas as pd
    df = pd.DataFrame({
        'dept': ['A', 'A', 'A'],
        'salary': [100, 300, 200]
    })
    result = fn(df)
    assert list(result['salary']) == [300, 200, 100]
