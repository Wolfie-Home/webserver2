#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from database.service.user import User as UserSvc
from database.service.location import Location as LocationSvc
from database.service.device import Device as DeviceSvc
from database.service.property import Property as PropertySvc
from database.datatype import DataType
from database.service.exceptions import AlreadyExistsError, NoRecordError

if __name__ == '__main__':
    """
    Create user
    """
    try:
        user = UserSvc.create('defaultUser', 'dummypassword', 'kbumsik@gmail.com')
    except AlreadyExistsError as error:
        print(error)
        print('user already exists...')
    else:
        print('user creation success!')
    finally:
        try:
            user = UserSvc.verify('defaultUser', 'dummypassword')
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
        location_tmp = LocationSvc.create('defaultHouse', user.id, description="This is default house")
    except AlreadyExistsError as error:
        print(error)
        print('Default House already exists...')
    else:
        print('Default House creation success!')
    finally:
        try:
            house = LocationSvc.get(user.id, name='defaultHouse')
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
            location_tmp.extend(LocationSvc.create('defaultRoom' + str(idx), user.id,
                                                house_id=house.id,
                                                description="This is default room"+str(idx)))
    except AlreadyExistsError as error:
        print(error)
        print('Rooms already exists...')
    else:
        print('3 Rooms creation success!')
    finally:
        try:
            rooms = LocationSvc.get_list(user.id, house_id=house.id)
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
        datatype_tmp = DataType.create('integer', "A JSON Integer Type")
        print(datatype_tmp)
        datatype_tmp = DataType.create('number', "A JSON Floating point number Type")
        print(datatype_tmp)
        datatype_tmp = DataType.create('string', "A JSON String Type")
        print(datatype_tmp)
        datatype_tmp = DataType.create('boolean', "A JSON Boolean Type")
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
        encoded = DataType.encode["integer"](34633)
        decoded = DataType.decode["integer"]("34633")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        # float
        encoded = DataType.encode[2](0.00764535)
        decoded = DataType.decode[2]("0.00764535")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        encoded = DataType.encode["number"](0.00764535)
        decoded = DataType.decode["number"]("0.00764535")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        # str
        encoded = DataType.encode[3]("str string")
        decoded = DataType.decode[3]("str string")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        encoded = DataType.encode["string"]("str string")
        decoded = DataType.decode["string"]("str string")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        # bool
        encoded = DataType.encode[4](False)
        decoded = DataType.decode[4]("False")
        print(type(encoded), encoded)
        print(type(decoded), decoded)
        encoded = DataType.encode["boolean"](False)
        decoded = DataType.decode["boolean"]("False")
        print(type(encoded), encoded)
        print(type(decoded), decoded)

    """
    Create a device
    """
    property_list = [
        {"type": "boolean", "name": "switch", "controllable": False, "description": "Default switch"},
        {"type": "integer", "name": "Green", "controllable": True, "description": "Default greed color value"},
        {"type": "number", "name": "temp", "controllable": False, "description": "Default temperature value"},
        {"type": "string", "name": "msg", "controllable": True, "description": "Default messages to device"}
    ]
    try:
        device_tmp1 = DeviceSvc.create('defaultDevice1', user.id, property_list,
                                      description="This is default device in nowhere")
        device_tmp2 = DeviceSvc.create('defaultDevice2', user.id, property_list, location_id=house.id,
                                       description="This is default device #1 in the house")
        device_tmp3 = DeviceSvc.create('defaultDevice3', user.id, property_list, location_id=house.id,
                                       mother_id=device_tmp2.id,
                                       description="This is default device #2 in the house")
        device_tmp4 = DeviceSvc.create('defaultDevice4', user.id, property_list, location_id=rooms[0].id,
                                       description="This is default device #1 in room 1")
        device_tmp5 = DeviceSvc.create('defaultDevice5', user.id, property_list, location_id=rooms[0].id,
                                       mother_id=device_tmp4.id,
                                       description="This is default device #2 in room 1")
        device_tmp6 = DeviceSvc.create('defaultDevice6', user.id, property_list, location_id=rooms[0].id,
                                       mother_id=device_tmp4.id,
                                       description="This is default device #3 in room 1")
        device_tmp7 = DeviceSvc.create('defaultDevice7', user.id, property_list, location_id=rooms[1].id,
                                       description="This is default device #1 in room 2")
        device_tmp8 = DeviceSvc.create('defaultDevice8', user.id, property_list, location_id=rooms[1].id,
                                       description="This is default device #2 in room 2")
        device_tmp9 = DeviceSvc.create('defaultDevice9', user.id, property_list, location_id=rooms[2].id,
                                       description="This is default device #1 in room 3")
    except AlreadyExistsError as error:
        print(error)
        print('Default device already exists...')
    else:
        print('Default device creation success!')
    finally:
        try:
            device = DeviceSvc.get(user.id, name='defaultDevice1')
            parameters = PropertySvc.get_list(user.id, device.id)
        except NoRecordError as error:
            print(error)
            print('Device retrieve failed')
        else:
            print('Device retrieve success!')
            print(device)
            for param in parameters:
                print(param)
    pass
