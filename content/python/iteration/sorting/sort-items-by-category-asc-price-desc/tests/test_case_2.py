def test_case_2():
    assert equal(sort_items_by_category_asc_price_desc(**{'items': [{'name': 'Solo', 'category': 'M', 'price': 42}]}), [{'name': 'Solo', 'category': 'M', 'price': 42}])
