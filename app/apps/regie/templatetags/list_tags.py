from django import template

register = template.Library()


@register.filter
def is_list(element):
    list_types = (list, tuple)
    return type(element) in list_types
