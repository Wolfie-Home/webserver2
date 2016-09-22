"""
To define a new datatype, you need to make encoder and decoder
functions.
"""


def integer_encode(value):
    return str(value)


def integer_decode(value):
    return int(value)


def number_encode(value):
    return '{:e}'.format(float(value))


def number_decode(value):
    return float(value)


def string_encode(value):
    return str(value)


def string_decode(value):
    return str(value)


def boolean_encode(value):
    return str(value)


def boolean_decode(value):
    if value == 'False':
        return False
    elif value == 'True':
        return True
    return bool(value)



