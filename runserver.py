#!/usr/bin/env python3
from flask import Flask
from wolfie_home.webpages import webpage
from wolfie_home.api_web import webapi
import os

# server setting
static_folder_path = 'wolfie_home/static'   # static files (e.g. js files...) path
app = Flask(__name__, static_folder=static_folder_path)
app.secret_key = os.urandom(24)    # set the secret key. This is used for session. Keep this really secret
enable_debugging = True

# register blueprints
app.register_blueprint(webpage)
app.register_blueprint(webapi)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=enable_debugging)
