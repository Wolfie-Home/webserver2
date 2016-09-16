class DBServiceError(Exception):
    """
    Base exception of database service
    """
    def __init__(self, message):
        self.message = str(message)

    def __str__(self, *args, **kwargs):
        return self.message
    pass


class AlreadyExistsError(DBServiceError):
    """
    Usually happens when there is a key already exists
    """
    pass


class NoRecordError(DBServiceError):
    """
    Database returns nothing
    """
    pass


class UnknownError(DBServiceError):
    """
    Unknown database error
    """
    def __init__(self, message):
        self.message = 'Unknown service error: ' + str(message)


def assert_NoRecord(expression, errmsg):
    if expression is None:
        raise NoRecordError(errmsg)
