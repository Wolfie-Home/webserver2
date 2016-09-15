from .service import user as UserSvc


class User:
    def __init__(self):
        """
        just make all attributes to NULL.
        """
        self.id = None          # integer, unique
        self.username = None   # string, unique
        self.password = None    # string
        self.email = None       # string
        pass

    @classmethod
    def create(cls, username, password, email):
        """
        Create an user into DB.
        :param username: username to create
        :param password: password
        :param email: email
        :return: new User object without password
        """
        result = UserSvc.create(username, password, email)
        # construct a new object
        new = cls()
        new.id = result['Id']
        new.username = result['UserName']
        new.email = result['Email']
        return new

    @classmethod
    def login(cls, username, password):
        """
        lookup user.
        :param username: username to lookup
        :param password: password
        :return: new User object without password
        """
        result = UserSvc.login(username, password)
        # construct a new object
        new = cls()
        new.id = result['Id']
        new.username = result['UserName']
        new.email = result['Email']
        return new
