"""
model.Location
"""


class Location:
    def __init__(self, **kwargs):
        """
        just make all attributes to NULL.
        """
        self.id = kwargs["id"]              # integer, unique
        self.name = kwargs["name"]            # string
        self.user_id = kwargs["user_id"]         # integer, reference to User.id
        self.description = kwargs["description"]     # string
        self.house_id = kwargs["house_id"]        # integer, reference to self.id
        self.house = kwargs.get("house", None)        # integer, reference to self.id
        self.rooms = []
        pass

    def __iter__(self):
        yield 'id',             self.id
        yield 'name',           self.name
        yield 'user_id',        self.user_id
        yield 'description',    self.description
        yield 'house_id',       self.house_id
        yield 'house',          self.house
        rooms_list = []
        for child in self.rooms:
            rooms_list.append(dict(child))
        yield 'rooms', rooms_list
        pass

    def __str__(self):
        string = "Location ID: " + str(self.id) + ", Name: " + str(self.name) + \
                    ", Owner ID: " + str(self.user_id) + ", Parent location ID: " + str(self.house_id) + \
                    ", Description: " + str(self.description)
        return string
    pass
