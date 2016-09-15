from flask import Blueprint, request, session
from flask import abort, Response
import json

from database.models import User

webapi = Blueprint('web_api', __name__, template_folder='templates')


@webapi.route('/api/login', methods=['POST'])
def login():
    content = request.form
    # verify from db
    try:
        user = User.verify(content['username'], content['password'])
    except:
        abort(400)
    if user.username != content['username']:
        abort(400)
    session['username'] = content['username']

    # return json response
    payload = json.dumps({'username': user.username})
    response = Response(
        response=payload,
        status=200,
        mimetype='application/json; charset=utf-8'
    )
    return response


@webapi.route('/api/logout', methods=['POST'])
def logout():
    # remove the username from the session if it's there
    user = session.pop('username', None)

    # return json response
    payload = json.dumps({'username': user})
    response = Response(
        response=payload,
        status=200,
        mimetype='application/json; charset=utf-8'
    )
    return response


"""
The following codes is used for debugging purpose.
"""
from runserver import enable_debugging

if enable_debugging:
    @webapi.before_request
    def before():
        print("============================")
        print("Printing request:")
        print("Headers:\n", request.headers)
        print("Payload:\n", request.get_data())
        print("Printing response done.")
        print("============================")
        pass


    @webapi.after_request
    def after(response):
        print("============================")
        print("Printing response:")
        print("Status:\n", response.status)
        print("Headers:\n", response.headers)
        print("Payload:\n", response.get_data())
        print("Printing response done.")
        print("============================")
        return response
