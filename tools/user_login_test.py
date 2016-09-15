#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from database.models import User

if __name__ == '__main__':
    try:
        user = User.create('kbumsik', 'dummypass', 'kbumsik@gmail.com')
    except Exception:
        print('user already exists...trying login anyway')
    else:
        print('user creation success!')
        print(user.id, user.user_name, user.email, user.password)

    try:
        user = User.login('kbumsik', 'dummypass')
    except Exception:
        print('login failed')
    else:
        print('login success!')
        print(user.id, user.user_name, user.email, user.password)
    pass
