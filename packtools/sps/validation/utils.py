def format_response(
        title,
        item,
        sub_item,
        validation_type,
        is_valid,
        expected,
        obtained,
        advice):
    return {
                'title': title,
                'item': item,
                'sub-item': sub_item,
                'validation_type': validation_type,
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected,
                'got_value': obtained,
                'message': f'Got {obtained}, expected {expected}',
                'advice': None if is_valid else advice
            }
