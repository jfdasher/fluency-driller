def test_case_3():
    assert equal(name_score_dict(**{'names': ['ann', 'ben'], 'scores': [0, 100]}), {'ann': 0, 'ben': 100})
