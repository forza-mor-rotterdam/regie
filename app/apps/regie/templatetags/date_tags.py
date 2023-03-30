from datetime import datetime

from django import template

register = template.Library()


@register.filter
def to_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
    except Exception as e:
        print(e)
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
