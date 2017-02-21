#!/usr/bin/python3

from flask import Flask


from wolfie_home.webpages import webpage
from wolfie_home.api_web import webapi
from wolfie_home.api_device import devapi
import os

# server setting
import settings
app = Flask(__name__, static_folder=settings.static_folder_path)
app.secret_key = os.urandom(24)    # set the secret key. This is used for session. Keep this really secret

# register blueprints
app.register_blueprint(webpage)
app.register_blueprint(webapi)
app.register_blueprint(devapi)


if __name__ == '__main__':
    # start app
    app.run(host='0.0.0.0', port=8000, debug=settings.enable_debugging)

