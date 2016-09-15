from .service import user as UserSvc


class User:
    def __init__(self):
        """
        just make all attributes to NULL.
        """
        self.id = None          # integer, unique
        self.user_name = None   # string, unique
        self.password = None    # string
        self.email = None       # string
        pass

    @classmethod
    def create(cls, user_name, password, email):
        """
        Create an user into DB.
        :param user_name: username to create
        :param password: password
        :param email: email
        :return: new User object without password
        """
        result = UserSvc.create(user_name, password, email)
        # construct a new object
        new = cls()
        new.id = result['Id']
        new.user_name = result['UserName']
        new.email = result['Email']
        return new

    @classmethod
    def login(cls, user_name, password):
        """
        lookup user.
        :param user_name: username to lookup
        :param password: password
        :return: new User object without password
        """
        result = UserSvc.login(user_name, password)
        # construct a new object
        new = cls()
        new.id = result['Id']
        new.user_name = result['UserName']
        new.email = result['Email']
        return new
