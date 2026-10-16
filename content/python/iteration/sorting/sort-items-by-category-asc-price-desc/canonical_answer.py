def sort_items_by_category_asc_price_desc(items):
    step1 = sorted(items, key=lambda x: x['price'], reverse=True)
    step2 = sorted(step1, key=lambda x: x['category'])
    return step2
