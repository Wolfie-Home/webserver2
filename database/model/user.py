"""
model.User
"""


class User:
    def __init__(self, **kwargs):
        """
        just make all attributes to NULL.
        """
        self.id = kwargs["id"]          # integer, unique
        self.username = kwargs["username"]   # string, unique
        self.password = kwargs.get("password", None)    # string
        self.email = kwargs["email"]       # string
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
    pass

