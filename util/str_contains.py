def str_contains(haystack, needle):
    return haystack.find(needle) >= 0


def str_contains_ignore_case(haystack, needle):
    return str_contains(haystack.lower(), needle.lower())
