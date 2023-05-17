import base64
from re import sub

from django.core.files.storage import default_storage
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


def to_base64(file):
    binary_file = default_storage.open(file)
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode("utf-8")
    return base64_message
