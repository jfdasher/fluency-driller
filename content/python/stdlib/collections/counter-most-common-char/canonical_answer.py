from collections import Counter

def most_common_char(s):
    return Counter(s).most_common(1)[0][0]
