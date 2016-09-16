import json
from flask import Response


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
