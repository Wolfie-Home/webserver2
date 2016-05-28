from django.http import HttpResponse
from wolfie_db import WolfieDB, WolfieUsersDB, WolfieHouseDB
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import logging

db_users = WolfieUsersDB()
db_house = WolfieHouseDB()

def login(request):
    logging.info('receive a login request')
    resp = HttpResponse()
    if not request.method == 'POST' or \
       not request.POST.has_key('username') or \
       not request.POST.has_key('password'):
        logging.warning('invalid login request')
        resp.status_code = 400
        return resp

    password = request.POST['password']
    username = request.POST['username']
    ret, user = db_users.get_user_by_username(username)
    if not ret or user['password'] != password:
        logging.warning('wrong password, %s, for user %s', password, username)
        resp.status_code = 400
        return resp

    resp.status_code = 301
    resp.set_cookie('username', value=username)
    logging.info('%s login successfully', username)
    return resp



def logout(request):
    logging.info('receive logout request')
    resp = HttpResponse()
    if not request.method == 'POST' or \
       not request.COOKIES.has_key('username'):
        logging.warning('invalid logout request')
        resp.status_code = 400
        return resp

    logging.info('logout successfully')        
    resp.delete_cookie('username')
    resp.status_code = 200
    return resp
    


def house(request):
    logging.info('receive house request')
    resp = HttpResponse()
    if not request.method == 'POST' or \
       not request.COOKIES.has_key('username'):
        logging.warning('invalid house request')
        resp.status_code = 400
        return resp

    ret, user = db_users.get_user_by_username(request.COOKIES['username'])
    if not ret:
        logging.warning('invalid username cookie')
        resp.status_code = 400
        return resp

    house_info = json.dumps(user['house_info'])
    resp.write(house_info)
    resp.status_code = 200
    logging.info('house request process succussfully')
    return resp
        


#  TODO verify the house is indeed the user's
def control(request):
    logging.info('receive control request')
    resp = HttpResponse()
    if not request.COOKIES.has_key('username') or \
       not request.method == 'POST' or \
       not request.POST.has_key('topic') or \
       not request.POST.has_key('payload'):
        logging.warning('invalid control request')
        resp.status_code = 400
        return resp

    topic = request.POST['topic']
    payload = request.POST['payload']
    publish.single(topic, payload=payload, qos=0, retain=False, hostname='localhost', port=1883)
    resp.status_code = 200
    logging.info('control request process successfully')
    return resp


# TODO need to verify the request belongs to the user.
def module(request):
    def ret_resp(status_code, modules=None, error_code=None, error_msg=None):
        '''
        @status_code, integer
        @modules, string, json format
        @error_code, integer
        @error_msg, string
        returns an instance of HttpResponse
        '''
        resp = HttpResponse()
        if status_code == 400:
            error = {
                'error_code': error_code,
                'error_msg': error_msg
            }
            resp.write(json.dumps(error))
            resp.status_code = 400
            return resp
        elif status_code == 200:
            resp.write(modules)
            resp.status_code = 200
            return resp
        
    logging.info('receive module request')

    if not request.COOKIES.has_key('username') or \
       not request.method == 'POST' or \
       not request.POST.has_key('command') or \
       not request.POST.has_key('module_uids') or \
       not request.POST.has_key('modules'):
        logging.warning('invalid module request')
        return ret_resp(400, error_code=1, error_msg='invalid module request')

    command = request.POST['command']
    module_uids = request.POST['module_uids']
    modules = request.POST['modules']
    modules_uids_tokens = module_uids.split(',')
    modules_tokens = modules.split(',')
    if len(modules_uids_tokens) != len(modules_tokens):
        return ret_resp(400, error_code=1, error_msg='different length of tokens')

    if command == 'get_module_recent':
        modules_data = []
        for i in range(len(modules_uids_tokens)):
            module_data = []
            ret, data = db_house.get_module(modules_uids_tokens[i], modules_tokens[i])
            if not ret:
                logging.warning('failed to query in module request')
                return ret_resp(400, error_code=2, error_msg='fail to query')
            module_data.append(
                {
                    'timestamp': data['time'],
                    'uid': data['uid'],
                    'module': data['module'],
                    'content': data['mod_content']
                }
            )
        modules_data.append(module_data)
        return ret_resp(200, modules=json.dumps(modules_data))

    elif command == 'get_module_all':
        modules_data = []
        for i in range(len(modules_uids_tokens)):
            module_data = []
            cols = {
                'uid': modules_uids_tokens[i],
                'module': modules_tokens[i]
            }
            ret, data = db_house.get_module(modules_uids_tokens[i], modules_tokens[i])
            if not ret:
                logging.warning('failed to query all in module request')
                return ret_resp(400, error_code=2, error_msg='fail to query all')

            for m in data:
                module_data.append(
                    {
                        'timestamp': m['time'],
                        'uid': m['uid'],
                        'module': m['module'],
                        'content': m['mod_content']
                    }
                )
        modules_data.append(module_data)
        return ret_resp(200, modules=json.dumps(modules_data))
        
    else:
        logging.warning('invalid module request, invalid command')
        return ret_resp(400, error_code=1, error_msg='invalid command in module req')


