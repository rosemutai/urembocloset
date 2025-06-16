from django import template

register = template.Library()

@register.filter(name='add_class_attribute')
def add_class_attribute(field, css):
    return field.as_widget(attrs={'class': css})