def test_case_4():
    assert equal(sort_people_by_age_then_name(**{'people': [['Nina', 35], ['Liam', 28], ['Olivia', 28], ['Noah', 35]]}), [['Liam', 28], ['Olivia', 28], ['Nina', 35], ['Noah', 35]])
