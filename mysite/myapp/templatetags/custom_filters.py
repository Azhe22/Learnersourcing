from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_value_from_list(lst, index):
    try:
        return lst[index]
    except (IndexError, TypeError):
        return None