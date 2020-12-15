import re


def decoder(pattern, string):
    matches = re.findall(pattern=pattern, string=string)
    return matches[0] if matches else None
