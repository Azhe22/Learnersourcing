from django import template

register = template.Library()


@register.filter
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0  # Return 0 or any default value if conversion fails
