from database.service import location as LocationSvc


class Location:
    def __init__(self):
        """
        just make all attributes to NULL.
        """
        self.id = None              # integer, unique
        self.name = None            # string
        self.user_id = None         # integer, reference to User.id
        self.description = None     # string
        self.house_id = None        # integer, reference to self.id
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
    def create(cls, name, user_id, house_id=None, description=''):
        """
        Create a new location
        :param name: name of location
        :param userid: Owner id
        :param parentid: Parent location id
        :param description: short description
        :return: new Location instance.
        """
        result = LocationSvc.create(name, user_id, house_id, description)
        # construct a new object
        new = cls()
        # key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        new.id = result['Id']
        new.name = result['Name']
        new.user_id = result['UserRef']
        new.description = result['Description']
        new.house_id = result['Parent']
        return new

    @classmethod
    def get(cls, user_id, locationid=None, name=None):
        """
        Lookup a single location
        :param user_id: owner's id
        :param locationid: id. Optional
        :param name: name of location, Optional
        :return: new Location instance.
        """
        result = LocationSvc.get(user_id, locationid, name)
        # construct a new object
        new = cls()
        # key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        new.id = result[0]['Id']
        new.name = result[0]['Name']
        new.user_id = result[0]['UserRef']
        new.description = result[0]['Description']
        new.house_id = result[0]['Parent']
        return new

    @classmethod
    def get_list(cls, user_id, house_id=None):
        """
        Get list of locations
        :param user_id: owner's id
        :param house_id: parent location id, optional.
        :return: new list of location instances.
        """
        result = LocationSvc.get(user_id, parentid=house_id)
        # construct a new object
        new_list = []
        # key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        for obj in result:
            new = cls()
            new.id = obj['Id']
            new.name = obj['Name']
            new.user_id = obj['UserRef']
            new.description = obj['Description']
            new.house_id = obj['Parent']
            new_list.append(new)
        return new_list
    pass