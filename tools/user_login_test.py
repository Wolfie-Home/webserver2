#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from database.models import User
from database.service.exceptions import AlreadyExistsError, NoRecordError

if __name__ == '__main__':
    try:
        user = User.create('defaultUser', 'dummypassword', 'kbumsik@gmail.com')
    except AlreadyExistsError as error:
        print(error)
        print('user already exists...trying login anyway')
    else:
        print('user creation success!')
        print(user.id, user.username, user.email, user.password)

    try:
        user = User.verify('defaultUser', 'dummypassword')
    except NoRecordError as error:
        print(error)
        print('login failed')
    else:
        print('login success!')
    print(user.id, user.username, user.email, user.password)
    pass
