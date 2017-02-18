"""
model.Device
"""


class Device:
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
        self.properties = []
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
        property_list = []
        for prop in self.properties:
            property_list.append(dict(prop))
        if len(property_list) != 0:
            yield 'properties', property_list
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
