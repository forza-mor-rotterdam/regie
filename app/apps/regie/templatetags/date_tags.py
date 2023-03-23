from django import template
from datetime import datetime

register = template.Library()


@register.filter
def to_date(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")