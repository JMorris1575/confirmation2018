from django import template
from ..models import Activity, Page, Response

register = template.Library()

@register.simple_tag
def activity_stats(stats, slug):
    return stats[slug]