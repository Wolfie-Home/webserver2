from flask import Blueprint, request, session

from database.service.location import Location as LocationSvc
from database.service.user import User as UserSvc
from database.service.device import Device as DeviceSvc
from database.service.property import Property as PropertySvc
from database.service.exceptions import NoRecordError
from wolfie_home.common import request_content_json, login_required_json
from wolfie_home.common import response_json_ok, response_json_error

devapi = Blueprint('device_api', __name__, template_folder='templates')

@devapi.route('/dev_api/<string:username>/<string:location_name>/<string:device_name>', methods=['POST'])
@request_content_json
def record_insert(content, username, location_name, device_name):
    """
    insert a record
    """
    # Get user id
    try:
        """
        Parameters requirements are here
        """
        user_id = session.get('user_id', None)
        if not user_id:
            password = content.get("password")
            user = UserSvc.verify(username, password)
            user_id = user.id
    except NoRecordError as error:
        return response_json_error({}, str(error))  # Usually username password mismatch
    except Exception:
        return response_json_error({}, "Wrong parameter")

    # Get location, deices ids
    try:
        location = LocationSvc.get(user_id, name=location_name)
        device = DeviceSvc.get(user_id, name=device_name)
    except NoRecordError as error:
        return response_json_error({}, str(error))  # No record

    # Not put data in there
    try:
        PropertySvc.save_record_dict(device.id, location.id, content.get("content"))
    except Exception:
        return response_json_error({}, "Wrong parameter")

    return response_json_ok({}, "Insertion good")

"""
The following codes is used for debugging purpose.
"""
from runserver import enable_debugging

if enable_debugging:
    @devapi.before_request
    def before():
        print("============================")
        print("Printing request:")
        print("Headers:\n", request.headers)
        print("Payload:\n", request.get_data())
        print("Printing response done.")
        print("============================")
        pass


    @devapi.after_request
    def after(response):
        print("============================")
        print("Printing response:")
        print("Status:\n", response.status)
        print("Headers:\n", response.headers)
        print("Payload:\n", response.get_data())
        print("Printing response done.")
        print("============================")
        return response
