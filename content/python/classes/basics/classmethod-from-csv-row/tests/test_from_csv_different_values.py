def test_from_csv_different_values():
    e = Employee.from_csv('Eve,Marketing,61000')
    assert e.name == 'Eve'
    assert e.department == 'Marketing'
    assert e.salary == 61000.0
