from django import template

register = template.Library()

@register.filter
def format_url_path(value):
    value = value.strip('/')
    if not value:
        return 'Home'
    parts = value.split('/')
    return ' / '.join(part.capitalize() for part in parts)