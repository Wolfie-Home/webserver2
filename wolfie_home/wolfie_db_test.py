# testing wolfie_db.

import logging
import json
from wolfie_db import WolfieDB 

logging.basicConfig(filename='wolfie_db_test.log', \
                    format='%(levelname)s,%(asctime)s,%(filename)s:%(message)s', \
                    level=logging.NOTSET)

db = WolfieDB()
# house_info = '''
# {
#     "house_name": "jack_house",
#     "mod_list": [
# 	{
# 	    "uid": "1038592",
# 	    "module": "wireless",
# 	    "location": "living room"
# 	}
#     ]
# }
# '''
# inserted_data = {
#     'username': 'jack',
#     'password': '123456',
#     'email': '123456wolfie@gmail.com',
#     'house_info': house_info
# }

# # QUERY_USER_INSERT
# (status, _) = db.query_user(WolfieDB.QUERY_USER_INSERT, inserted_data)
# if status == False:
#     print "status is False?"
# else:
#     print "success"

# # QUERY_USER_GET
# (status, data) = db.query_user(WolfieDB.QUERY_USER_GET, {'username': 'jack'})
# if status == False:
#     print "status is False?"
# else:
#     print "success"
#     print data

# QUERY_HOUSE_INSERT
mod_content = '''
{
    "Btyp": 1,
    "Bater": 43
}
'''
inserted_data = {
    'house': 'jack_house',
    'uid': '12345678',
    'module': 'battery',
    'mod_content': mod_content
}
r = db.query_house(WolfieDB.QUERY_HOUSE_INSERT, inserted_data)
print "HOUSE_INSERT returns: %s" % str(r)

# QUERY_HOUSE_GET_ALL
r = db.query_house(WolfieDB.QUERY_HOUSE_GET_ALL, {'uid': '12345678', 'module': 'battery'})
print "HOUSE_GET_ALL returns: %s" % str(r)

# QUERY_HOUSE_GET
r = db.query_house(WolfieDB.QUERY_HOUSE_GET, {'uid': '12345678', 'module': 'battery'})
print "HOUSE_GET returns: %s" % str(r)

