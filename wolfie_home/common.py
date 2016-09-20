import json
from flask import Response

"""
functions for JSON response
"""

def response_json(dict_data, status):
    payload = json.dumps(dict_data)
    response = Response(
        response=payload,
        status=status,
        mimetype='application/json; charset=utf-8'
    )
    return response


def response_json_ok(dict_data, message):
    dict_data["msg"] = message
    return response_json(dict_data, 200)


def response_json_error(dict_data, message):
    dict_data["errmsg"] = message
    return response_json(dict_data, 400)

"""
Decorator functions
"""
from functools import wraps
from flask import request, session, redirect, url_for


def login_required_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id', None) is None:
            return response_json_error({}, "Login first")
        return f(*args, **kwargs)
    return decorated_function


def login_required_redirect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id', None) is None:
            return redirect(url_for('web_pages.main'))
        return f(*args, **kwargs)
    return decorated_function


def request_content_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            content = request.get_json()
        except:
            return response_json_error({}, "Please send request in application/json")
        return f(content, *args, **kwargs)
    return decorated_function


# FIXME: For some reason, request.form is not working well...
def request_content_xWwwFormUrlEncoded_and_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        content = request.form
        if not content:
            try:
                content = request.get_json()
            except:
                return response_json_error({}, "Format your request")
        return f(content, *args, **kwargs)
    return decorated_function
