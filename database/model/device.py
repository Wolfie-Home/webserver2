from database.service import device as DeviceSvc


class Device:
    def __init__(self):
        """
        just make all attributes to NULL.
        """
        self.id = None              # integer, unique
        self.name = None            # string
        self.user_id = None         # integer, reference to User.id
        self.class_id = None          # TODO: Implement device class
        self.description = None     # string
        self.mother_id = None        # integer, reference to self.id
        self.location = None
        self.location_id = None
        self.values = None          # TODO: utilize this
        pass

    def __iter__(self):
        yield 'id',          self.id
        yield 'name',        self.name
        yield 'user_id',     self.user_id
        yield 'description', self.description
        yield 'house_id',    self.house_id
        pass

    def __str__(self):
        string = "Location ID: " + str(self.id) + ", Name: " + str(self.name) + \
                    ", Owner ID: " + str(self.user_id) + ", Parent location ID: " + str(self.house_id) + \
                    ", Description: " + str(self.description)
        return string

    @classmethod
    def create(cls, name, user_id, class_id=None, location_id=None, mother_id=None, description=''):
        """
        Create a new location
        :param name: name of location
        :param userid: Owner id
        :param parentid: Parent location id
        :param description: short description
        :return: new Location instance.
        """
        result = DeviceSvc.create(name, user_id, location_id, mother_id, description)
        # construct a new object
        new = cls()
        # key = (`Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`)
        new.id = result['Id']
        new.name = result['Name']
        new.user_id = result['OwnerRef']
        # new.class_id =    # FIXME: add device class
        new.description = result['Description']
        new.mother_id = result['Parent']
        # new.location =  # FIXME: add name of location
        new.location_id = result['LocationRef']
        # new.values =  # FIXME: add name values
        return new

    @classmethod
    def get(cls, user_id, device_id=None, name=None):
        """
        Lookup a single location
        :param user_id: owner's id
        :param locationid: id. Optional
        :param name: name of location, Optional
        :return: new Location instance.
        """
        result = DeviceSvc.get(user_id, device_id, name)
        # construct a new object
        new = cls()
        # key = (`Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`)
        new.id = result['Id']
        new.name = result['Name']
        new.user_id = result['OwnerRef']
        # new.class_id =    # FIXME: add device class
        new.description = result['Description']
        new.mother_id = result['Parent']
        # new.location =  # FIXME: add name of location
        new.location_id = result['LocationRef']
        # new.values =  # FIXME: add name values
        return new

    @classmethod
    def get_list(cls, user_id, mother_id=None, location_id=None):
        """
        Get list of locations
        :param user_id: owner's id
        :param house_id: parent location id, optional.
        :return: new list of location instances.
        """
        result = DeviceSvc.get(user_id, parentid=mother_id, locationid=location_id)
        # construct a new object
        new_list = []
        # key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        for obj in result:
            new = cls()
            # key = (`Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`)
            new.id = obj['Id']
            new.name = obj['Name']
            new.user_id = obj['OwnerRef']
            # new.class_id =    # FIXME: add device class
            new.description = obj['Description']
            new.mother_id = obj['Parent']
            # new.location =  # FIXME: add name of location
            new.location_id = obj['LocationRef']
            # new.values =  # FIXME: add name values
            new_list.append(new)
        return new_list
    pass
