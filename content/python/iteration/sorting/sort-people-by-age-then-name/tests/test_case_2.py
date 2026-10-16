def test_case_2():
    assert equal(sort_people_by_age_then_name(**{'people': [['Tom', 40]]}), [['Tom', 40]])
