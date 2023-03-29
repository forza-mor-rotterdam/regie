from django import template

register = template.Library()


@register.filter
def qs_ordenen(qs_huidige, orden_param):
    qs_huidige_dict = qs_huidige.to_dict()
    qs_huidige_dict.update({"ordering": orden_param})
    return qs_huidige_dict.to_qs()
