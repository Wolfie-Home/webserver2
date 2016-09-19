#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from database.model.user import User
from database.model.location import Location
from database.datatype import DataType
from database.service.exceptions import AlreadyExistsError, NoRecordError

if __name__ == '__main__':
    """
    Create user
    """
    try:
        user = User.create('defaultUser', 'dummypassword', 'kbumsik@gmail.com')
    except AlreadyExistsError as error:
        print(error)
        print('user already exists...')
    else:
        print('user creation success!')
    finally:
        try:
            user = User.verify('defaultUser', 'dummypassword')
        except NoRecordError as error:
            print(error)
            print('login failed')
        else:
            print('login success!')
            print(user)

    """
    Create house
    """
    try:
        location_tmp = Location.create('defaultHouse', user.id, description="This is default house")
    except AlreadyExistsError as error:
        print(error)
        print('Default House already exists...')
    else:
        print('Default House creation success!')
    finally:
        try:
            house = Location.get(user.id, name='defaultHouse')
        except NoRecordError as error:
            print(error)
            print('House retrieve failed')
        else:
            print('House retrieve success!')
            print(house)

    """
    Create rooms
    """
    try:
        location_tmp = []
        for idx in range(1, 4):
            location_tmp.extend(Location.create('defaultRoom' + str(idx), user.id,
                                                house_id=house.id,
                                                description="This is default room"+str(idx)))
    except AlreadyExistsError as error:
        print(error)
        print('Rooms already exists...')
    else:
        print('3 Rooms creation success!')
    finally:
        try:
            rooms = Location.get_list(user.id, house.id)
        except NoRecordError as error:
            print(error)
            print('Room retrieve failed')
        else:
            print('3 Rooms retrieve success!')
            for room in rooms:
                print(room)

    """
    Create datatypes.
    We are printing them many times to check if it is singletone
    """
    try:
        datatype_tmp = DataType.create('int', "Integer Type")
        print(datatype_tmp)
        datatype_tmp = DataType.create('float', "Floating point number Type")
        print(datatype_tmp)
        datatype_tmp = DataType.create('str', "String Type")
        print(datatype_tmp)
        datatype_tmp = DataType.create('bool', "Boolean Type")
        print(datatype_tmp)
    except AlreadyExistsError as error:
        print(error)
        print("Datatypes already exists")
    finally:
        datatype_tmp = DataType.get()
        print(datatype_tmp)
        datatype_tmp = DataType.get()
        print(datatype_tmp)

        print("Data conversion test:")
        # int
        encoded = DataType.encode[1](34633)
        decoded = DataType.decode[1]("34633")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        encoded = DataType.encode["int"](34633)
        decoded = DataType.decode["int"]("34633")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        # float
        encoded = DataType.encode[2](0.00764535)
        decoded = DataType.decode[2]("0.00764535")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        encoded = DataType.encode["float"](0.00764535)
        decoded = DataType.decode["float"]("0.00764535")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        # str
        encoded = DataType.encode[3]("str string")
        decoded = DataType.decode[3]("str string")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        encoded = DataType.encode["str"]("str string")
        decoded = DataType.decode["str"]("str string")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        # bool
        encoded = DataType.encode[4](False)
        decoded = DataType.decode[4]("False")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        encoded = DataType.encode["bool"](False)
        decoded = DataType.decode["bool"]("False")
        print(type(encoded), encoded)
        print(type(decoded), decoded)

    pass
