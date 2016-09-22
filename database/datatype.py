from database.settings import singletone
from database import datatype_functions
from database.service.datatype import DataType as DataTypeSvc


@singletone
class DataType:
    """
    This model is very different from others, because DataType model is singletone
    """
    datatypes = {}     # list of __Properties
    decode = {}
    encode = {}
    __updated = False

    class __Properties:
        def __init__(self, **kwargs):
            self.id = kwargs['id']                    # integer, unique
            self.name = kwargs['name']                # string
            self.description = kwargs['description']  # string

    def __init__(self):
        self.update()
        pass

    def __str__(self):
        string = repr(self)
        return string

    def get(self):
        DataType.update()
        return self

    @classmethod
    def create(cls, name, description):
        """
        Create a new location
        :param name: name of location
        :param userid: Owner id
        :param parentid: Parent location id
        :param description: short description
        :return: new Location instance.
        """
        DataTypeSvc.create(name, description)
        cls.__updated = False
        cls.update()
        return cls

    @classmethod
    def update(cls):
        """
        Update singletone
        :return:
        """
        if not cls.__updated:
            result = DataTypeSvc.get_list()
            for obj in result:
                # update list
                new = cls.__Properties(**obj)
                cls.datatypes[new.name] = new
                cls.datatypes[new.id] = new
                # update encoder
                cls.encode[new.name] = getattr(datatype_functions, new.name + "_encode")
                cls.encode[new.id] = getattr(datatype_functions, new.name + "_encode")
                # update decoder
                cls.decode[new.name] = getattr(datatype_functions, new.name + "_decode")
                cls.decode[new.id] = getattr(datatype_functions, new.name + "_decode")
            cls.__updated = True
        return cls
    pass
