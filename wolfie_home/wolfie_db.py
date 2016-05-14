import mysql.connector
import logging
import json

class WolfieDB():
    '''
    Careful!! all query statement are not escaped, which is vulenerable
    to attacks.
    Q:
    1. under what circumstances, reconnect will fail?
    one connection can only work with one table? too many reuqests will 
    get rejected?
    '''
    USERS_TABLE = 'users'
    HOUSE_TABLE = 'house'

    QUERY_USER_INSERT = 0
    QUERY_USER_GET = 1

    QUERY_HOUSE_INSERT = 2
    QUERY_HOUSE_GET = 3
    QUERY_HOUSE_GET_ALL = 4
    
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
            
    def __check_conn(self):
        '''
        check if the mysql connection is still on. if not, it tries to 
        reconnect, then gives up it still can not connect.
        return True on success, False otherwise.
        '''
        if self.conn.is_connected():
            return True
        try:
            self.conn.get_rows()
        except Exception as e:
            logging.warning(str(e))

        logging.warning('lose connection, and try to reconnect')
        if self.conn.reconnect(attempts=3, delay=100) == True:
            logging.warning('reconnect successfully')
            return True
        else:
            try:
                # reconstruct a mysql connection
                re_conn = mysql.connector.connect(**self.config)
            except Error as e:
                # even this failed...
                logging.warning('failed to reconnect')
                return False
            logging.warning('re-create a connection successfully')
            self.conn = re_conn
            return True

    def query_user(self, cmd, columns):
        '''
        perform mysql statement on user table. proper use of this methond should
        not throw an exception.
        @cmd: QUERY_USER_INFO_INSERT, insert a new user. QUERY_USER_INFO_GET
            query information about a user
        @columns: type is dictionary. data of each columns. if @cmd is 
            QUERY_USER_GET, only username is needed.
        return a tuple: (bool, data). bool indicate if query exceeds. when 
            QUERY_USER_GET is used, data returns a dictionary representing
            the row.
        '''
        if self.__check_conn() == False:
            logging.warning('connection failed')
            return False, None

        if cmd == WolfieDB.QUERY_USER_INSERT:
            # build insert statement
            statement = 'INSERT INTO %s ' %  WolfieDB.USERS_TABLE + \
                 '(username, password, email, house_info) ' + \
                 'VALUES (\'%s\', \'%s\', \'%s\', \'%s\')' \
                 % (columns['username'], columns['password'], columns['email'], \
                    columns['house_info'])
            try:
                self.conn.cmd_query(statement)
                self.conn.commit()
            except Exception as e:
                logging.warning('error when trying to insert a row to users table: %s', str(e))
                return False, None
            logging.info('insert a data to users table')
            return True, None

        elif cmd == WolfieDB.QUERY_USER_GET:
            # query
            statement = 'SELECT * FROM %s WHERE username=\'%s\'' \
                        % (WolfieDB.USERS_TABLE, columns['username'])
            self.conn.cmd_query(statement) # this should not throw exception
            (data, _) = self.conn.get_row()
            if data == None:
                return False, None
            user_info = dict()
            user_info['uid'] = int(data[0])
            user_info['username'] = str(data[1])
            user_info['password'] = str(data[2])
            user_info['email'] = str(data[3])
            user_info['house_info'] = json.loads(str(data[4]))
            return True, user_info

        else:
            logging.error('query_user is entered invalid command');
            raise Exception('invalid commnad\n')


    def query_house(self, cmd, columns):
        '''
        query related to house table.
        @cmd, three possible commands, QUERY_HOUSE_INSERT, QUERY_HOUSE_GET
              QUERY_HOUSE_GET_ALL. QUERY_HOUSE_INSERT insert a new module into 
              the database. QUERY_HOUSE_GET gets the most recent data about a module.
              QUERY_HOUSE_GET_ALL get all data about a module.
        @columns, dict, depending on the cmd.
        @return, (status, data)
        '''            
        if self.__check_conn() == False:
            logging.warning('connection failed')
            return False, None

        if cmd == WolfieDB.QUERY_HOUSE_INSERT:
            '''
            @columns['house'], house name
            @columns['uid'], uid id
            @columns['module'], module type
            @columns['mod_content'], module type
            @return (status, data). data is None
            '''
            statement = ('INSERT INTO %s (house, uid, module, mod_content) ' + \
                 'VALUES (\'%s\', \'%s\', \'%s\', \'%s\')')\
                 % (WolfieDB.HOUSE_TABLE, columns['house'], columns['uid'], \
                     columns['module'], columns['mod_content'])
            try:
                self.conn.cmd_query(statement)
                self.conn.commit()
            except Exception as e:
                logging.warning('error when trying to insert a row to house table: %s', str(e))
                return False, None
            logging.info('insert a data to house table')
            return True, None

        elif cmd == WolfieDB.QUERY_HOUSE_GET:
            '''
            get the most recent data about a module
            @columns['uid'], the identifier of the module
            @columns['module'], the module type
            @return, (status, data). status is boolean, and data is a dict. 
            '''
            statement = ('SELECT * FROM %s WHERE uid=\'%s\' AND module=\'%s\'' \
                        + 'ORDER BY time DESC LIMIT 1') \
                        % (WolfieDB.HOUSE_TABLE, columns['uid'], columns['module'])
            self.conn.cmd_query(statement) # this should not throw exception
            (data, _) = self.conn.get_row()
            if data == None:
                return False, None
            module_info = dict()
            module_info['house'] = str(data[0])
            module_info['uid'] = str(data[1])
            module_info['module'] = str(data[2])
            module_info['mod_content'] = json.loads(str(data[3]))
            module_info['time'] = str(data[4])
            return True, module_info

        elif cmd == WolfieDB.QUERY_HOUSE_GET_ALL:
            '''
            similar to QUERY_HOUSE_GET. but the data is not recent one of the module,
            it is all data of that module.
            '''
            statement = ('SELECT * FROM %s WHERE uid=\'%s\' AND module=\'%s\'') \
                        % (WolfieDB.HOUSE_TABLE, columns['uid'], columns['module'])
            self.conn.cmd_query(statement) # this should not throw exception
            data, _ = self.conn.get_rows()
            if data == []:
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
            return True, module_info_all

        else:
            logging.error('invalid command in query_house')
            raise Exception('invalid commnad.\n')



            
            
                

                


