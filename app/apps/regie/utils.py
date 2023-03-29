from re import sub

from django.http import QueryDict


def snake_case(s: str) -> str:
    return "_".join(
        sub(
            "([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", s.replace("-", " "))
        ).split()
    ).lower()


def dict_to_querystring(d: dict) -> str:
    return "&".join([f"{p}={v}" for p, l in d.items() for v in l])


def querystring_to_dict(s: str) -> dict:
    return dict(QueryDict(s))
