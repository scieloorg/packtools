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


def multiple_fields(keys, values):
    """
    {
        "k": "0000-0002-6656-8155",
        "n": "Adriana Valongo",
        "1": "aff3",
        "s": "Zani",
        "r": "ND",
        "_": ""
    },
    """
    d = {}
    for key, value in zip(keys, values):
        if value is not None:
            d[key] = value
    return d
