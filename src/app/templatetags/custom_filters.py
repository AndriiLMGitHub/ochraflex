import re
from django import template

register = template.Library()


@register.simple_tag
def is_active_path(request, pattern):
    """
    Перевіряє, чи поточний шлях відповідає регулярному виразу.
    """
    return "active" if re.match(pattern, request.path) else ""
