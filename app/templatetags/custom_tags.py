from django import template
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def permissionFlag(val):
    return val

@register.filter(name='split')
def split(str):
    return str.split(',')

@register.filter(name='nbsp')
def nbsp(value):
    return mark_safe("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join(value.split('  ')))