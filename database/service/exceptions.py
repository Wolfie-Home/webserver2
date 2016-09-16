class AlreadyExistsError(Exception):
    """
    Usually happens when there is a key already exists
    """
    pass


class NoRecordError(Exception):
    """
    Database returns nothing
    """
    pass


class UnknownError(Exception):
    """
    Unknown database error
    """
    pass
