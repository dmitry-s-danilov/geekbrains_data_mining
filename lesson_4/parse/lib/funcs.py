from re import findall


def find(pattern, string):
    matches = findall(pattern=pattern, string=string)
    return matches[0] if matches else None
