def sort_people_by_age_then_name(people):
    return sorted(people, key=lambda p: (p[1], p[0]))
