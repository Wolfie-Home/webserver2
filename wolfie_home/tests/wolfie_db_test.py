################################################################
# test wolfie_db.py
########################################################
import logging
import json
from unittest import TestCase
from django.test import Client
from threading import Thread, Lock
import thread

# include the module being tested
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(  \
    os.path.abspath(__file__))))
from wolfie_db2 import WolfieUsersDB, WolfieHouseDB


logging.basicConfig(filename='wolfie_db_test.log', \
                    format='%(levelname)s,%(asctime)s,%(filename)s' \
                    + 'at line %(lineno)s:%(message)s', \
                    level=logging.NOTSET)


class WolfieUsersDBTest(TestCase):
    def setUp(self):
        self.users_db = WolfieUsersDB()

    def test_users(self):
        # creating a new user
        # assume this will generate a uid
        uid = str(random.random()) 
        username = 'Mike'+uid
        password = uid
        email = uid+'@gmail.com'
        house_name: 'mike'+uid+'_house'
        house_info = 'none'
        ret = self.users_db.create_new_user(username, password, email, house_info)
        # tiny chance of fasle negative, due to non-unique uid
        self.assertTrue(ret)

        # getting user
        ret = self.users_db.get_user_by_username(username)
        self.assertTrue(ret[0]) 
        user = json.loads(ret[1])
        self.assertEqual(user['username'], username) 
        self.assertEqual(user['password'], password) 
        self.assertEqual(user['email'], email)

    def test_users_stress(self):
        # stress tests on users. multiple threads to interact with DB
        # NOTE: threads has its own 'exception context', meaning only
        #       one thead only catch its own exception.
        pass                    # TODO



class WolfieHouseDBTestCase(TestCase):
    def setUp(self):
        self.house_db = WolfieHouseDB()
        
    def test_house(self):
        house = 'jack_house'
        uid = str(random.random())
        module = 'battery'
        mod_content = {
            'Btyp': 2,
            'Bater': 43,
        }
        # test create_module_data
        ret = self.house_db.create_module_data(house, uid, module, json.dumps(mod_content))
        self.assertTrue(ret)
        # test get_module
        ret = self.house_db.get_module(uid, module)
        self.assertTrue(ret[0])
        self.assertEqual(ret[1]['house'], house)
        self.assertEqual(ret[1]['mod_content']['Btyp'], 2)
        self.assertEqual(ret[1]['mod_content']['Bater'], 43)
        # test get_module_all
        ret = self.house_db.get_module_all(uid, module)
        self.assertTrue(ret[0])
        self.assertTrue(len(ret[1]) > 0)

    def test_house_stress(self):
        def make_query_function(db, lock, i, uid, module, mod_content):
            def fxn():
                global WolfieHouseDBTestCase_failed
                try: 
                    ret = db.get_module(uid, module)
                except Exception as e:
                    WolfieHouseDBTestCase_failed = True
                    raise e
                lock.acquire(True)
                if ret[0] == False:
                    WolfieHouseDBTestCase_failed = True
                else:
                    if (ret[1]['mod_content'] != mod_content):
                        WolfieHouseDBTestCase_failed = True

!!                        raise Exception('mod_content is not right')

            return fxn
        # create data in the database first
        house = 'jack_house'
        uid = str(random.random())
        module = 'battery'
        mod_content = {
            'Btyp': 2,
            'Bater': 43,
        }
        ret = self.house_db.create_module_data(house, uid, module, json.dumps(mod_content))
        self.assertTrue(ret)
        # global variable for threads to notified the main thread
        global WolfieHouseDBTestCase_failed = False
        threads = []
        lock = Lock()
        n = 100
        for i in range(n):
            f = make_query_function(house_db, lock, i, '1', 'battery')
            thread = Thread(target=f)
            thds.append(thread)
        for t in thds:
            t.start()
        
        
    


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




################################################################
# test wolfie_db.py
########################################################
import logging
import json
from unittest import TestCase
from django.test import Client
from threading import Thread, Lock
import thread

# include the module being tested
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(  \
    os.path.abspath(__file__))))
from wolfie_db2 import WolfieUsersDB, WolfieHouseDB


logging.basicConfig(filename='wolfie_db_test.log', \
                    format='%(levelname)s,%(asctime)s,%(filename)s' \
                    + 'at line %(lineno)s:%(message)s', \
                    level=logging.NOTSET)


class WolfieUserTest(TestCase):
    def setUp(self):
        users_db = WolfieUsersDB()

    def test_users(self):
        # creating a new user
        # assume this will generate a uid
        uid = str(random.random()) 
        username = 'Mike'+uid
        password = uid
        email = uid+'@gmail.com'
        house_name: 'mike'+uid+'_house'
        house_info = 'none'
        ret = self.users_db.create_new_user(username, password, email, house_info)
        # tiny chance of fasle negative, due to non-unique uid
        self.assertEqual(ret, True) 

        # getting user
        ret = self.users_db.get_user_by_username(username)
        self.assertEqual(ret[0], True) 
        user = json.loads(ret[1])
        self.assertEqual(user['username'], username) 
        self.assertEqual(user['password'], password) 
        self.assertEqual(user['email'], email)

    def test_users_stress(self):
        # stress tests on users. multiple threads to interact with DB
        # NOTE: threads has its own 'exception context', meaning only
        #       one thead only catch its own exception.
        
        


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
