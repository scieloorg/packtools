def simple_field(key, value):
    if value:
        return {
                key: [
                    {
                        "_": value
                    }
                ]
            }
    return {}

def complex_field(key, value):
    if value:
        return {
                key: [
                   value
                ]
            }
    return {}

def add_item(dictionary, key, value):
    if value is not None:
        dictionary[key] = value

def multiple_complex_field(key, value_list):
    if value_list:
        return {
                key: value_list
            }
    return {}