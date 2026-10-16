def test_from_csv_basic():
    e = Employee.from_csv('Alice,Engineering,95000')
    assert e.name == 'Alice'
    assert e.department == 'Engineering'
    assert e.salary == 95000.0
