"""
model.Property
"""


class Property:
    class Record:
        def __init__(self, **kwargs):
            """
            just make all attributes to NULL.
            """
            self.value = kwargs["value"]  # Flexible type based on datatype.py
            self.time = kwargs["time"]  # integer, reference to User.id
            pass

        def __iter__(self):
            yield 'value', self.value
            yield 'time', self.time

        def __str__(self):
            string = "Vale: " + str(self.value) + ", Time: " + str(self.time)
            return string
        pass

    def __init__(self, **kwargs):
        """
        just make all attributes to NULL.
        """
        self.name = kwargs["name"]  # string
        self.type = kwargs["type"]  # integer, reference to User.id
        self.controllable = kwargs["controllable"]  # TODO: Implement device class
        self.description = kwargs["description"]  # string
        self.records = []  # Record subclass

        pass

    def __iter__(self):
        yield 'name', self.name
        yield 'type', self.type
        yield 'controllable', self.controllable
        yield 'description', self.description
        record_list = []
        for record in self.records:
            record_list.append(dict(record))
        yield 'records', record_list


    def __str__(self):
        string = "Name: " + str(self.name) + ", Type: " + str(self.type) + \
                 ", Controllable: " + str(self.controllable) + \
                 ", Description: " + str(self.description)
        return string

    pass
