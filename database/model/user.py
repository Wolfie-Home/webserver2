from database.service import user as UserSvc


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

    def __iter__(self):
        yield 'id',          self.id
        yield 'username',        self.username
        yield 'password',     self.password
        yield 'email', self.email
        pass

    def __str__(self):
        string = "User ID: " + str(self.id) + ", Name: " + str(self.username) + \
                    ", Email: " + str(self.email)
        return string

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
    def verify(cls, username, password):
        """
        lookup user.
        :param username: username to lookup
        :param password: password
        :return: new User object without password
        """
        result = UserSvc.verify(username, password)
        # construct a new object
        new = cls()
        new.id = result['Id']
        new.username = result['UserName']
        new.email = result['Email']
        return new
    pass

