def test_case_0():
    assert equal(name_score_dict(**{'names': ['alice', 'bob', 'carol'], 'scores': [95, 82, 78]}), {'alice': 95, 'bob': 82, 'carol': 78})
