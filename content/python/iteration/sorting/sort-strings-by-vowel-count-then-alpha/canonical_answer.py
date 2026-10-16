def sort_strings_by_vowel_count_then_alpha(words):
    return sorted(words, key=lambda w: (sum(c in 'aeiou' for c in w), w))
