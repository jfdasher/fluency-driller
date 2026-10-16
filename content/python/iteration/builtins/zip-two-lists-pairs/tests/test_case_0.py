def test_case_0():
    assert equal(pair_names_scores(**{'names': ['Alice', 'Bob', 'Carol'], 'scores': [95, 82, 78]}), [['Alice', 95], ['Bob', 82], ['Carol', 78]])
