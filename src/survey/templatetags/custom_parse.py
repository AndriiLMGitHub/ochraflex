from django import template
import json

register = template.Library()

@register.filter
def json_loads(value):
    """
    Розпаковує список, який містить рядок JSON-представлення списку рядків.
    """
    try:
        if isinstance(value, list) and len(value) == 1:
            inner_list_str = value[0]
            return json.loads(inner_list_str)
        return value  # Повертає початкове значення, якщо структура не відповідає очікуваній
    except (TypeError, json.JSONDecodeError, IndexError):
        return value  # Повертає початкове значення в разі помилки