from django import template
from ..models import Activity, Page, Response

register = template.Library()

@register.simple_tag
def dict_read(dictionary, current_key):
    return dictionary[current_key]