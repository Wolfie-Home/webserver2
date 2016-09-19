from database.settings import singletone
from database import datatype_functions
from database.service import datatype as DataTypeSvc


@singletone
class DataType:
    """
    This model is very different from others, because DataType model is singletone
    """
    datatypes = []     # list of __Properties
    decode = {}
    encode = {}
    __updated = False

    class __Properties:
        def __init__(self, idx, name, description):
            self.id = idx                   # integer, unique
            self.name = name                # string
            self.description = description  # string

    def __init__(self):
        pass

    def __str__(self):
        string = repr(self)
        return string

    def get(self):
        DataType.update()
        return self

    def create(self, name, description):
        """
        Create a new location
        :param name: name of location
        :param userid: Owner id
        :param parentid: Parent location id
        :param description: short description
        :return: new Location instance.
        """
        DataTypeSvc.create(name, description)
        DataType.__updated = False
        DataType.update()
        return self

    def update(self):
        """
        Update singletone
        :return:
        """
        if not DataType.__updated:
            result = DataTypeSvc.get_list()
            # key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
            for obj in result:
                # update list
                new = DataType.__Properties(obj['Id'], obj['TypeName'], obj['Description'])
                DataType.datatypes.append(new)
                # update encoder
                DataType.encode[new.name] = getattr(datatype_functions, new.name + "_encode")
                DataType.encode[new.id] = getattr(datatype_functions, new.name + "_encode")
                # update decoder
                DataType.decode[new.name] = getattr(datatype_functions, new.name + "_decode")
                DataType.decode[new.id] = getattr(datatype_functions, new.name + "_decode")
            DataType.__updated = True
        return self
    pass
