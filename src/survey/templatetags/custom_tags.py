from django import template
from collections import defaultdict

register = template.Library()

@register.simple_tag
def group_by_combined_block(field_responses):
    """Групує field_responses за combined_block"""
    grouped_data = defaultdict(list)

    for field_response in field_responses:
        if field_response.combined_block:
            grouped_data[field_response.combined_block].append(field_response)

    return grouped_data.items()  # Повертає список кортежів (combined_block, field_responses)
