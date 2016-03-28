import mysql.connector
import logging
import json

class WolfieDB():
    '''
    Careful!! all query statement are not escaped, which is vulenerable
    to attacks.
    '''
    USERS_TABLE = 'users'

    QUERY_USER_INSERT = 0
    QUERY_USER_GET = 1
    
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
        self.conn = mysql.connector.connect(**config)
            
    def __check_conn(self):
        '''
        check if the mysql connection is still on. if not, it tries to 
        reconnect, then gives up it still can not connect.
        return True on success, False otherwise.
        '''
        ret = self.conn.is_connected():
        self.conn.get_rows()
        if ret == True:
            return True

        logging.warning('lose connection, and try to reconnect')
        ret = self.conn.reconnect(attempts=3, delay=0)
        self.conn.get_rows()
        if ret == True:
            logging.warning('reconnect successfully')
            return True
        else:
            logging.warning('failed to reconnect')
            return False


    def query_user(self, cmd, columns):
        '''
        perform mysql statement on user table. proper use of this methond should
        not throw an exception.
        @cmd: QUERY_USER_INFO_INSERT, insert a new user. QUERY_USER_INFO_GET
            query information about a user
        @columns: type is dictionary. data of each columns. if @cmd is 
            QUERY_USER_INFO_GET, only uid is needed.
        return a tuple: (bool, data). bool indicate if query exceeds. when 
            QUERY_USER_INFO_GET is used, data returns a dictionary representing
            the row.
        '''
        if self.__check_conn() == False:
            return False, None

        if cmd == QUERY_USER_INSERT:
            # checking columns. only simple type checks.
            if type(columns) != dict or not columns.has_key('username') or \
               not columns.has_key('email')  or not columns.has_key('wolfie_home') or \
               not columns.has_key('devices'):
                logging.error('parameters are not right');
                raise Exception('parameter error\n')
            if type(columns['username']) != str or columns['username'] == '' or \
               type(columns['password']) != str or columns['password'] == '' or \
               type(columns['email']) != str or columns['email'] == '' or \
               type(columns['wolfie_home']) != str or columns['wolfie_home'] == '' or \
               type(columns['devices']) != str or columns['devices'] == '':
                logging.error('parameters are not right');
                raise Exception('parameter error\n')

            # build insert statement
            statement = 'INSERT INTO %s ' % USERS_TABLE + \
                 '(username, password, email, wolfie_home, devices) ' + \
                 'VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' \
                 % (columns['username'], columns['password'], columns['email'], \
                    columns['wolfie_home'], columns['devices'])
            try:
                self.conn.cmd_query(statement)
                self.conn.commit()
            except Exception as e:
                logging.warning('error when trying to insert a row: %s', str(e))
                return False, None
            logging.info('insert a query')
            return True, None

        else if cmd == QUERY_USER_GET:
            # parameter type checking
            if type(columns) != dict or not columns.has_key('username') or \
               type(columns['username']) != str:
                logging.error('parameters are not right');
                raise Exception('parameter error\n')
            # query
            statement = 'SELECT * FROM users WHERE username=%s' % (columns['username'])
            self.conn.cmd_query(statement) # this should not throw exception
            (data, _) = self.conn.get_row()
            if data == None:
                return False, None
            user_info = dict()
            user_info['uid'] = int(data[0])
            user_info['username'] = str(data[1])
            user_info['password'] = str(data[2])
            user_info['email'] = str(data[3])
            user_info['wolfie_home'] = str(data[4])
            user_info['devices'] = json.loads(data[5])
            return True, user_info

        else:
            logging.error('query_user is entered invalid command');
            raise Exception('invalid commnad\n')


            


                

                


