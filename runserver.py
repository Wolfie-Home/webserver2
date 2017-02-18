#!/usr/bin/python3

from flask import Flask

enable_debugging = True
GATEWAY_ADDR = '127.0.0.1'
GATEWAY_PORT = 9999

from wolfie_home.webpages import webpage
from wolfie_home.api_web import webapi
from wolfie_home.api_device import devapi
import os

# server setting
static_folder_path = 'wolfie_home/static'   # static files (e.g. js files...) path
app = Flask(__name__, static_folder=static_folder_path)
app.secret_key = os.urandom(24)    # set the secret key. This is used for session. Keep this really secret

# register blueprints
app.register_blueprint(webpage)
app.register_blueprint(webapi)
app.register_blueprint(devapi)

# Set MQTT client
import paho.mqtt.client as mqtt
from wolfie_home.api_mqtt import mqtt_on_connect
mqtt_client = mqtt.Client()

if __name__ == '__main__':
    mqtt_client.on_connect = mqtt_on_connect
    try:
        mqtt_client.connect(host="127.0.0.1", port=1883, keepalive=60)
    except:
        print('Failed to connect to the server')
        exit()
    else:
        print('Connection Success!')
    print('MQTT connection is being ready...')
    mqtt_client.loop_start()

    app.run(host='0.0.0.0', port=8000, debug=enable_debugging)
