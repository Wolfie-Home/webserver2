import paho.mqtt
from database.service.location import Location as LocationSvc
from database.service.user import User as UserSvc
from database.service.device import Device as DeviceSvc
from database.service.property import Property as PropertySvc
from database.service.exceptions import NoRecordError

# The callback for when the client receives a CONNACK response from the server.
def mqtt_on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("record/#")
    client.on_message = mqtt_on_message

import json
import re
record_insert_regex = re.compile("record\/(\w+)\/(\w+)\/(\w+)")

# The callback for when a PUBLISH message is received from the server.
def mqtt_on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload
    matched = record_insert_regex.match(topic)
    json_payload = json.loads(payload)
    if matched:
        username = matched.group(1)
        location_name = matched.group(2)
        device_name = matched.group(3)
        # Get user id
        try:
            password = json_payload["password"]
            user = UserSvc.verify(username, password)
            user_id = user.id
        except NoRecordError as error:
            print(error)
            return # Usually username password mismatch
        except Exception as error:
            print(error)
            return
        # Get location, deices ids
        try:
            location = LocationSvc.get(user_id, name=location_name)
            device = DeviceSvc.get(user_id, name=device_name)
        except NoRecordError as error:
            print(error)
            return # No record

        # Not put data in there
        try:
            PropertySvc.save_record_dict(device.id, location.id, json_payload["content"])
        except Exception as error:
            print(error)
            return
    print("MQTT received. Topic: " + str(topic) + " Payload: " + str(payload))