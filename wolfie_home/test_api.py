import api
from unittest import TestCase
from django.test import Client
from django.core.urlresolvers import resolve
import jsonschema
import json


class ApiLoginTest(TestCase):
    def setUp(self):
        self.client = Client()  # act as a browser
        
    def test_url_resolve(self):
        found = resolve('/api/login')
        self.assertEqual(found.func, api.login)

    def test_login_failure(self):
        # fail. no POST fields are specified.
        post_data = {}
        resp = self.client.post('/api/login', post_data)
        self.assertEqual(resp.status_code, 400)
        # fail 2
        post_data = {'username': 'jack', 'password': '123456'}
        resp = self.client.get('/api/login', post_data)
        self.assertEqual(resp.status_code, 400)
        # fail 3
        post_data = {'username': 'jack', 'password': '123'}
        resp = self.client.post('/api/login', post_data)
        self.assertEqual(resp.status_code, 400)

    def test_login_success(self):
        # fail 3
        post_data = {'username': 'jack', 'password': '123456'}
        resp = self.client.post('/api/login', post_data)
        self.assertEqual(resp.status_code, 301)
        # TODO no sure how to test cookies

        resp = self.client.post('/api/logout')
        self.assertEqual(resp.status_code, 200)


class ApiLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()  # act as a browser

        
    def test_url_resolve(self):
        found = resolve('/api/logout')
        self.assertEqual(found.func, api.logout)


    def test_logout(self):
        # fail 1
        resp = self.client.get('/api/logout')
        self.assertEqual(resp.status_code , 400)
        # fail 2
        resp = self.client.post('/api/logout')
        self.assertEqual(resp.status_code , 400)

        # this should succeed
        post_data = {'username': 'jack', 'password': '123456'}
        resp = self.client.post('/api/login', post_data)
        self.assertEqual(resp.status_code, 301)

        resp = self.client.post('/api/logout')
        self.assertEqual(resp.status_code, 200)

class ApiHouseTest(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_url_resolve(self):
        found = resolve('/api/house')
        self.assertEqual(found.func, api.house)
    
    def test_house(self):
        # fail 1
        resp = self.client.get('/api/house')
        self.assertEqual(resp.status_code , 400)
        # fail 2
        resp = self.client.post('/api/house')
        self.assertEqual(resp.status_code , 400)

        # login, then query should succeed
        post_data = {'username': 'jack', 'password': '123456'}
        resp = self.client.post('/api/login', post_data)
        self.assertEqual(resp.status_code, 301)

        resp = self.client.post('/api/house')
        self.assertEqual(resp.status_code, 200)
        
        house_info = json.loads(resp.content())
        f = open('schema/house_info.json', 'r')
        house_schema = json.load(f)
        jsonschema.validate(house_info, house_schema)
        f.close()

        # logout
        resp = self.client.post('/api/logout')
        self.assertEqual(resp.status_code, 200)


class ApiModulesTest(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_url_resolve(self):
        foundn = resolve('/api/module')
        self.assertEqaul(found.func, api.module)

    def test_module_failure(self):
        resp = self.client.get('/api/module')
        self.assertEqual(resp.status_code, 400)
        req_data = {
            'command': 'get_module_recent',
            'module_uids' : '12345678',
            'modules': 'battery'
        }
        resp = self.client.get('/api/module', req_data)
        self.assertEqual(resp.status_code, 400)
        resp = self.client.post('/api/module', req_data)
        self.assertEqual(resp.status_code, 400)

        # login
        login_data = {'username': 'jack', 'password': '123456'}
        resp = self.client.post('/api/login', login_data)
        self.assertEqual(resp.status_code, 200)

        req_data = {
            'command': 'get_module_ecent',
            'module_uids' : '12345678',
            'modules': 'battery'
        }
        resp = self.client.post('/api/module', req_data)
        self.assertEqual(resp.status_code, 400)

        # logout
        resp = self.client.post('/api/logout')
        self.assertEqual(resp.status_code, 200)
        
    def test_module_success(self):
        # login
        login_data = {'username': 'jack', 'password': '123456'}
        resp = self.client.post('/api/login', login_data)
        self.assertEqual(resp.status_code, 200)

        f = open('testout/module','w')

        req_data = {
            'command': 'get_module_recent',
            'module_uids' : '12345678',
            'modules': 'battery'
        }
        resp = self.client.post('/api/module', req_data)
        self.assertEqual(resp.status_code, 200)
        # inspect result manually
        f.write('sending :\n')
        f.write('%s\n' % json.dumps(req_data))
        f.write('getting back:\n')
        f.write('%s\n', resp.content)
        f.write('------------------\n')

        req_data = {
            'command': 'get_module_recent_all',
            'module_uids' : '12345678,1244332',
            'modules': 'battery,environment'
        }
        resp = self.client.post('/api/module', req_data)
        self.assertEqual(resp.status_code, 200)
        # inspect result manually
        f.write('sending :\n')
        f.write('%s\n' % json.dumps(req_data))
        f.write('getting back:\n')
        f.write('%s\n', resp.content)
        f.write('------------------\n')
        
        f.close()

        # logout
        resp = self.client.post('/api/logout')
        self.assertEqual(resp.status_code, 200)

        
class ApiControlTest(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_url_resolve(self):
        found = resolve('/api/control')
        self.assertEqual(found.func, api.control)

    def test_control(self):
        payload = {
            'type':'control',
            'content': {
                'Hum': 10,
                'Tmp': 23,
                'Bar': 40
            }
        }
        control_data = {
            'topic': 'com/jack_house/1244332/environment',
            'payload': json.dumps(payload)
        }
        resp = self.client.get('/api/control', control_data)
        self.assertEqual(resp.status_code, 400)
        resp = self.client.post('/api/control', control_data)
        self.assertEqual(resp.status_code, 400)
        
        # login
        post_data = {'username': 'jack', 'password': '123456'}
        resp = self.client.post('/api/login', post_data)
        self.assertEqual(resp.status_code, 301)

        resp = self.client.post('/api/control', control_data)
        self.assertEqual(resp.status_code, 200)

        # logout
        resp = self.client.post('/api/logout')
        self.assertEqual(resp.status_code, 200)

        
        
        
