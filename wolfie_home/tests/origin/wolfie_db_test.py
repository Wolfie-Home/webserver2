# testing wolfie_db.

import logging
import json
from wolfie_db2 import WolfieUsersDB, WolfieHouseDB
from threading import Thread, Lock
import thread

logging.basicConfig(filename='wolfie_db_test.log', \
                    format='%(levelname)s,%(asctime)s,%(filename)s at line %(lineno)s:%(message)s',\
                    level=logging.NOTSET)

# testing WoflieUserDB
users_db = WolfieUsersDB()
username = 'mike'
password = '123456'
email = '123456mike@gmail.com'
house_info = '''
{
    'house_name': 'mike_house',
    'mod_list': [
	{
	    'uid': '1038592',
	    'module': 'wireless',
	    'location': 'living room'
	}
    ]
}
'''
# create_new_user
ret = users_db.create_new_user(username, password, email, house_info)
if ret == False:
    print 'create_new_user failed.'
else:
    print 'create_new_user succeeded.'

# get_user_by_username
ret = users_db.get_user_by_username(username)
if ret[0] == False:
    print 'get_user_by_username failed'
else:
    print '=========get_user_by_username succeeded=============='
    print ret[1]
    print '====================================================='


# test WolfieHouseDB
house_db = WolfieHouseDB()

house = 'jack_house'
uid = '12345678'
module = 'battery'
mod_content = '''
{
    'Btyp': 2,
    'Bater': 43
}
'''
ret = house_db.create_module_data(house, uid, module, mod_content)
if ret == False:
    print 'create_module_data failed.'
else:
    print 'create_module_data succeeded.'

# get_module_all
ret = house_db.get_module_all('1', 'battery')
if ret[0] == False:
    print 'get_module_all failed.'
else:
    print '==============get_module_all succeeded==============='
    print ret[1]
    print '====================================================='

# get_module
ret = house_db.get_module('1', 'battery')
if ret[0] == False:
    print 'get_module failed'
else:
    print '==============get_module succeeded==================='
    print ret[1]
    print '====================================================='

ret = house_db.get_module('2', 'security')
if ret[0] == False:
    print 'get_module failed'
else:
    print '==============get_module succeeded==================='
    print ret[1]
    print '====================================================='

ret = house_db.get_module('3', 'wireless')
if ret[0] == False:
    print 'get_module failed'
else:
    print '==============get_module succeeded==================='
    print ret[1]
    print '====================================================='

ret = house_db.get_module('4', 'speaker_led')
if ret[0] == False:
    print 'get_module failed'
else:
    print '==============get_module succeeded==================='
    print ret[1]
    print '====================================================='

ret = house_db.get_module('5', 'environment')
if ret[0] == False:
    print 'get_module failed'
else:
    print '==============get_module succeeded==================='
    print ret[1]
    print '====================================================='


# stress test 
def make_query_function(db, lock, i, uid, module):
    def fxn():
        ret = db.get_module(uid, module)
        lock.acquire(True)
        if ret[0] == False:
            print 'get_module failed'
        else:
            print '========get_module i=%d succeeded =============' % i
            print ret[1]
            print '====================================================='
        lock.release()
    return fxn
thds = []
lock = Lock()
n = 100
for i in range(n):
    f = make_query_function(house_db, lock, i, '1', 'battery')
    thread = Thread(target=f)
    thds.append(thread)
for t in thds:
    t.start()


def hi():
    print 'sss'
t = Thread(target=hi)
t.start()

# def fxn():
#     ret = db.get_module('1', 'battery')
#     while lock.acquire(True):
#         pass
#     if ret[0] == False:
#         print 'get_module failed'
#     else:
#         print '========get_module i=%d succeeded =============' % i
#         print ret[1]
#         print '====================================================='
#     lock.release()

# def hi(s):
#     print s

# thread.start_new_thread(hi, ('nihao',))

while True:
    pass
