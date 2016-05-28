import mysql.connector
import logging
import json
from threading import Lock

'''
Careful!! all query statement are not escaped, which is vulenerable
to attacks.
'''

class WolfieDB():
    '''
    base class.
    '''
    def __init__(self, config=None):
        '''
        throw an exception if failed. Otherwise, it succeeds.
        '''
        self.conn = None        # mysql connection
        if config == None:
            config = {
                'user': 'chaojie',
                'password': 'dummypass',
                'host': 'localhost',
                'database': 'wolfie_home',
                'raise_on_warnings': True,
            }
        self.config = config
        self.conn = mysql.connector.connect(**config)
        self.__lock = Lock()
        
    def check_conn(self):
        '''
        check if the mysql connection is still on. if not, it tries to 
        reconnect, then gives up it still can not connect.
        @return: True on success, False otherwise.
        '''
        self.__lock.acquire()
        if self.conn.is_connected():
            self.__lock.release()
            return True
        try:
            self.conn.get_rows()
        except Exception as e:
            pass

        logging.info('lost connection. trying to reconnect')
        if self.conn.reconnect(attempts=3, delay=1) == True:
            logging.info('reconnected successfully')
            self.__lock.release()
            return True
        else:
            try:
                logging.info('failed reconnecting. trying re-construct a connection')
                re_conn = mysql.connector.connect(**self.config)
            except Error as e:
                logging.warning('failed to re-construct a connection!')
                self.__lock.release()
                return False
            logging.info('re-create a connection successfully')
            self.conn = re_conn
            self.__lock.release()
            return True


class WolfieUsersDB(WolfieDB):
    '''
    a class perform queries related to Users table. This is thread safe.
    '''
    USERS_TABLE = 'users'

    def __init__(self, config=None):
        WolfieDB.__init__(self, config)
        self.lock = Lock()
    
    def create_new_user(self, username, password, email, house_info):
        '''
        create a new user.
        perform mysql statement on user table. proper use of this methond should
        not throw an exception. assuming input is correct
        @username: username of the user.
        @password: password.
        @email: email of the user.
        @house_info: JSON object for describing the user's house
        @return: bool, to indicate if query succeeded 
        '''
        self.lock.acquire()
        if self.check_conn() == False:
            logging.warning('connection failed while performing create_new_user')
            self.lock.release()
            return False
        # build insert statement
        statement = 'INSERT INTO %s ' %  WolfieUsersDB.USERS_TABLE + \
                    '(username, password, email, house_info) ' + \
                    'VALUES (\'%s\', \'%s\', \'%s\', \'%s\')' \
                    % (username, password, email, house_info)
        try:
            self.conn.cmd_query(statement)
            self.conn.commit()
        except Exception as e:
            logging.warning('error when create_new_user: %s.', str(e))
            self.lock.release()
            return False
        logging.info('create_new_user successfully.')
        self.lock.release()
        return True

    def get_user_by_username(self, username):
        '''
        query an user by username
        @return: (bool, data). bool indicate if query exceeds. data is a dictionary 
        representing the row.
        '''
        self.lock.acquire()
        if self.check_conn() == False:
            logging.warning('connection failed while performing get_user_by_username')
            self.lock.release()
            return False, None
        statement = 'SELECT * FROM %s WHERE username=\'%s\'' \
                    % (WolfieUsersDB.USERS_TABLE, username)
        try:
            # this should not throw exception
            self.conn.cmd_query(statement) 
        except Exception as e:
            logging.error('error when get_user_by_username: %s.', str(e))
            self.lock.release()
            return False, None
        try:
            (data, _) = self.conn.get_row()
        except Exception as e:
            logging.warning('error when get_user_by_username: %s.', str(e))
            self.lock.release()
            return False, None
        if data == None:
            self.lock.release()
            return False, None
        user_info = dict()
        user_info['uid'] = int(data[0])
        user_info['username'] = str(data[1])
        user_info['password'] = str(data[2])
        user_info['email'] = str(data[3])
        user_info['house_info'] = json.loads(str(data[4]))
        logging.info('get_user_by_username successfully.')
        self.lock.release()
        return True, user_info

class WolfieHouseDB(WolfieDB):
    '''
    a class perform queries related to House table. This is thread safe.
    '''
    HOUSE_TABLE = 'house'

    def __init__(self, config=None):
        WolfieDB.__init__(self, config)
        self.lock = Lock()

    def create_module_data(self, house, uid, module, mod_content):
        '''
        create one data entry for a module.
        @house: house name
        @uid: uid id
        @module: module type
        @mod_content: JSON for describe content of the module
        @return: bool, status
        '''
        self.lock.acquire()
        if self.check_conn() == False:
            logging.warning('connection failed while performing create_module_data')
            self.lock.release()
            return False
        statement = ('INSERT INTO %s (house, uid, module, mod_content) ' + \
                 'VALUES (\'%s\', \'%s\', \'%s\', \'%s\')')\
                 % (WolfieHouseDB.HOUSE_TABLE, house, uid, module, mod_content)
        try:
            self.conn.cmd_query(statement)
            self.conn.commit()
        except Exception as e:
            logging.warning('error when create_module_data: %s', str(e))
            self.lock.release()
            return False
        logging.info('create_module_data successfully')
        self.lock.release()
        return True


    def get_module(self, uid, module):
        '''
        get the most recent data about a module
        @uid: the identifier of the module
        @module: the module type
        @return: (status, data). status is boolean, and data is a dict. 
        '''
        self.lock.acquire()
        if self.check_conn() == False:
            logging.warning('connection failed while performing get_module')
            self.lock.release()
            return False, None
        statement = ('SELECT * FROM %s WHERE uid=\'%s\' AND module=\'%s\'' \
                    + 'ORDER BY time DESC LIMIT 1') \
                    % (WolfieHouseDB.HOUSE_TABLE, uid, module)
        try:
            # this should not throw exception
            self.conn.cmd_query(statement) 
        except Exception as e:
            logging.error('error when get_module: %s', str(e))
            self.lock.release()
            return False, None
        try:
            (data, _) = self.conn.get_row()
        except Exception as e:
            logging.warning('error when get_module: %s.', str(e))
            self.lock.release()
            return False, None
        if data == None:
            logging.warning('in get_module_all, return data is None.')
            self.lock.release()
            return False, None
        module_info = dict()
        module_info['house'] = str(data[0])
        module_info['uid'] = str(data[1])
        module_info['module'] = str(data[2])
        module_info['mod_content'] = json.loads(str(data[3]))
        module_info['time'] = str(data[4])
        logging.info('get_module successfully.')
        self.lock.release()
        return True, module_info

    def get_module_all(self, uid, module):
        '''
        get all data of a module.
        @uid: the identifier of the module
        @module: the module type
        @return: (status, data). status is boolean, and data is a list of dictionaries. 
        '''
        self.lock.acquire()
        if self.check_conn() == False:
            logging.warning('connection failed while performing get_module')
            self.lock.release()
            return False, None
        statement = ('SELECT * FROM %s WHERE uid=\'%s\' AND module=\'%s\'') \
                    % (WolfieHouseDB.HOUSE_TABLE, uid, module)
        try:
            # this should not throw exception
            self.conn.cmd_query(statement) 
        except Exception as e:
            logging.error('error when get_module_all: %s.', str(e))
            self.lock.release()
            return False, None
        try:
            data, _ = self.conn.get_rows()
        except Exception as e:
            logging.warning('error when get_module_all: %s.', str(e))
            self.lock.release()
            return False, None
        if data == []:
            logging.warning('in get_module_all, return data is None.')
            self.lock.release()
            return False, None
        module_info_all = []
        for i in range(len(data)):
            module_info = dict()
            module_info['house'] = str(data[i][0])
            module_info['uid'] = str(data[i][1])
            module_info['module'] = str(data[i][2])
            module_info['mod_content'] = json.loads(str(data[i][3]))
            module_info['time'] = str(data[i][4])
            module_info_all.append(module_info)
        logging.info('get_module_all successfully.')
        self.lock.release()
        return True, module_info_all
