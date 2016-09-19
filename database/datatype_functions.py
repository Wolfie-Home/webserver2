"""
To define a new datatype, you need to make encoder and decoder
functions.
"""


def int_encode(value):
    return str(value)


def int_decode(value):
    return int(value)


def float_encode(value):
    return '{:e}'.format(float(value))


def float_decode(value):
    return float(value)


def str_encode(value):
    return str(value)


def str_decode(value):
    return str(value)


def bool_encode(value):
    return str(value)


def bool_decode(value):
    if value == 'False':
        return False
    elif value == 'True':
        return True
    return bool(value)



