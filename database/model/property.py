"""
model.Property
"""


class Property:
    def __init__(self, **kwargs):
        """
        just make all attributes to NULL.
        """
        self.name = kwargs["name"]  # string
        self.type = kwargs["type"]  # integer, reference to User.id
        self.controllable = kwargs["controllable"]  # TODO: Implement device class
        self.description = kwargs["description"]  # string
        self.value = kwargs.get("value", None)  # integer, reference to self.id
        self.time = kwargs.get("time", None)
        self.data = []  # [] list of data
        pass

    def __iter__(self):
        yield 'name', self.name
        yield 'type', self.type
        yield 'controllable', self.controllable
        yield 'description', self.description
        yield 'value', self.value
        yield 'time', self.time

    def __str__(self):
        string = "Name: " + str(self.name) + ", Type: " + str(self.type) + \
                 ", Controllable: " + str(self.controllable) + \
                 ", Description: " + str(self.description)
        return string

    pass
