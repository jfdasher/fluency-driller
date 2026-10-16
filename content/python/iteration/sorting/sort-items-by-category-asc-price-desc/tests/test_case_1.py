def test_case_1():
    assert equal(sort_items_by_category_asc_price_desc(**{'items': [{'name': 'Alpha', 'category': 'Z', 'price': 5}, {'name': 'Beta', 'category': 'A', 'price': 99}, {'name': 'Gamma', 'category': 'A', 'price': 50}]}), [{'name': 'Beta', 'category': 'A', 'price': 99}, {'name': 'Gamma', 'category': 'A', 'price': 50}, {'name': 'Alpha', 'category': 'Z', 'price': 5}])
