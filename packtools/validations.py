def is_valid_value_for_pid_v2(value):
    if len(value or "") != 23:
        raise ValueError
    return True


VALIDATE_FUNCTIONS = dict((
    ("scielo_pid_v2", is_valid_value_for_pid_v2),
))
