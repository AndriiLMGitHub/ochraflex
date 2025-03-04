import json


def parse_json(array):
    for field in array:
        if field.field_type == 'select' or field.field_type == 'radio' or field.field_type == 'checkbox':
            field.options = json.loads(field.options[0])
    return array

# Example usage
def parse_json_field(field):
    if field.field_type == 'select' or field.field_type == 'radio' or field.field_type == 'checkbox':
        field.options = json.loads(field.options[0])
    return field
