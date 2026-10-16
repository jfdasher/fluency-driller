def first_occurrence_index(items: list) -> dict:
    result = {}
    for i, v in enumerate(items):
        if v not in result:
            result[v] = i
    return result
