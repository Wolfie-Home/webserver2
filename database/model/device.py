"""
model.Device
"""


class Device:
    class Parameter:
        def __init__(self, **kwargs):
            """
            just make all attributes to NULL.
            """
            self.name = kwargs["name"]            # string
            self.type = kwargs["type"]         # integer, reference to User.id
            self.controllable = kwargs["controllable"]          # TODO: Implement device class
            self.description = kwargs["description"]     # string
            self.value = kwargs.get("value", None)        # integer, reference to self.id
            self.time = kwargs.get("time", None)
            self.values = []          # [] list
            self.times = []           # [] list of timestamp
            pass

        def __iter__(self):
            yield 'name',          self.name
            yield 'type',          self.type
            yield 'controllable',      self.controllable
            yield 'description',   self.description
            yield 'value',     self.value
            yield 'time',      self.time
            yield 'values',        self.values
            yield 'times', self.times

        def __str__(self):
            string = "Name: " + str(self.name) + ", Type: " + str(self.type) + \
                     ", Controllable: " + str(self.controllable) + \
                     ", Description: " + str(self.description)
            return string
        pass

    def __init__(self, **kwargs):
        """
        just make all attributes to NULL.
        """
        self.id = kwargs["id"]                              # integer, unique
        self.name = kwargs["name"]                          # string
        self.user_id = kwargs.get("user_id", None)          # integer, reference to User.id
        self.class_id = kwargs.get("class_id", None)        # TODO: Implement device class
        self.description = kwargs.get("description", None)  # string
        self.mother_id = kwargs["mother_id"]            # integer, reference to self.id
        self.location = kwargs.get("location", None)
        self.location_id = kwargs["location_id"]
        self.parameters = []
        self.children = []
        pass

    def __iter__(self):
        yield 'id',          self.id
        yield 'name',        self.name
        yield 'user_id',     self.user_id
        yield 'class_id', self.class_id
        yield 'description',    self.description
        yield 'mother_id',     self.mother_id
        yield 'location',     self.location
        yield 'location_id', self.location_id
        parameter_list = []
        for param in self.parameters:
            parameter_list.append(dict(param))
        if len(parameter_list) != 0:
            yield 'parameters', parameter_list
        children_list = []
        for child in self.children:
            children_list.append(dict(child))
        yield 'children', children_list
        pass

    def __str__(self):
        string = "Device ID: " + str(self.id) + ", Name: " + str(self.name) + ", Class ID: " + str(self.class_id) + \
                    ", Owner ID: " + str(self.user_id) + ", Mother device ID: " + str(self.mother_id) + \
                    ", location ID: " + str(self.location_id) + ", Description: " + str(self.description)
        return string
    pass
