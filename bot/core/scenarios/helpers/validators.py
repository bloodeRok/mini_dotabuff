import re


def date_is_valid(date: str):
    pattern = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
    return pattern.match(date)
