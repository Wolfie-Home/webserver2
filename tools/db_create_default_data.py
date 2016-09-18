#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from database.models import User, Location
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
    pass
