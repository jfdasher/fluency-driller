from collections import defaultdict

def group_names_by_first_letter(names):
    groups = defaultdict(list)
    for name in names:
        groups[name[0].upper()].append(name)
    return {k: sorted(v) for k, v in groups.items()}
