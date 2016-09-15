#!/usr/bin/env python3
from flask import Flask
from wolfie_home.webpages import wolfie_home_page

app = Flask(__name__)
app.register_blueprint(wolfie_home_page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
