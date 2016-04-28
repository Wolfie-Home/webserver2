from django.http import HttpResponse
from wolfie_db import WolfieDB
import json
import paho.mqtt.publish as publish

db = WolfieDB()

def login(request):
    resp = HttpResponse()
    if not request.method == 'POST' or \
       not request.POST.has_key('username') or \
       not request.POST.has_key('password'):
        resp.status_code = 400
        return resp
    username = request.POST['username']
    password = request.POST['password']
    ret, data = db.query_user(WolfieDB.QUERY_USER_GET, {'username': username})
    if not ret or resp['password'] != password:
        resp.status_code = 400
        return resp
    resp.status_code = 301
    resp.set_cookie('username', value=username)
    return resp



def logout(request):
    resp = HttpResponse()
    if not request.method == 'POST' or \
       not request.COOKIES.has_key('username'):
        resp.status_code = 400
    else:
        resp.delete_cookie('username')
        resp.status_code = 200
    return resp


def house(request):
    resp = HttpResponse()
    if not request.method == 'POST' or \
       not request.COOKIES.has_key('username'):
        resp.status_code = 400
        return resp
    ret, data = db.query_user(WolfieDB.QUERY_USER_GET, \
                        {'username': request.COOKIES['username']})
    if not ret:
        resp.status_code = 400
        return resp
    house_info = json.dumps(data['house_info'])
    resp.write(house_info)
    resp.status_code = 200
    return resp
        

def control(request):
    resp = HttpResponse()
    if not request.method == 'POST' or \
       not request.POST.has_key('topic') or \
       not request.POST.has_key('payload'):
        resp.status_code = 400
        return resp
    topic = request.POST['topic']
    payload = request.POST['payload']
    publish.single(topic, payload=payload, qos=0)
    resp.status_code = 200
    return resp


def module(request):
    resp = HttpResponse()
    if not request.method != 'POST' or \
       not request.POST.has_key('command') or \
       not request.POST.has_key('module_uids') or \
       not request.POST.has_key('modules'):
        resp.status_code = 400
        return resp
    command = request.POST['command']
    module_uids = request.POST['module_uids']
    modules = request.POST['modules']
    modules_uids_tokens = modules.split(',')
    modules_tokens = modules.split(',')
    if len(modules_uids_tokens) != len(modules_tokens):
        resp.status_code = 400
        return resp
    for i in range(len(modules_uids_tokens)):
        db.


    
        

    
def control(request):
    return HttpResponse('from control')
