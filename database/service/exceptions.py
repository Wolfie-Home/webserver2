class DBServiceError(Exception):
    """
    Base exception of database service
    """
    def __init__(self, message='Database Error.'):
        self.message = str(message)

    def __str__(self, *args, **kwargs):
        return self.message
    pass


class AlreadyExistsError(DBServiceError):
    """
    Usually happens when there is a key already exists
    """
    def __init__(self, message='Key already exists'):
        self.message = str(message)


class NoRecordError(DBServiceError):
    """
    Database returns nothing
    """
    def __init__(self, message='No record found'):
        self.message = str(message)


class UnknownError(DBServiceError):
    """
    Unknown database error
    """
    def __init__(self, message=''):
        self.message = 'Unknown service error: ' + str(message)


def assert_NoRecord(expression, errmsg):
    if expression is None:
        raise NoRecordError(errmsg)
