def format_response(
        title=None,
        parent=None,
        parent_id=None,
        item=None,
        sub_item=None,
        validation_type=None,
        is_valid=None,
        expected=None,
        obtained=None,
        advice=None):
    return {
                'title': title,
                'parent': parent,
                'parent_id': parent_id,
                'item': item,
                'sub_item': sub_item,
                'validation_type': validation_type,
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected,
                'got_value': obtained,
                'message': f'Got {obtained}, expected {expected}',
                'advice': None if is_valid else advice
            }
