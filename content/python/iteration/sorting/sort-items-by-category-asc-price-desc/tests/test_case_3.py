def test_case_3():
    assert equal(sort_items_by_category_asc_price_desc(**{'items': [{'name': 'X', 'category': 'C', 'price': 1}, {'name': 'Y', 'category': 'C', 'price': 3}, {'name': 'Z', 'category': 'C', 'price': 2}]}), [{'name': 'Y', 'category': 'C', 'price': 3}, {'name': 'Z', 'category': 'C', 'price': 2}, {'name': 'X', 'category': 'C', 'price': 1}])
