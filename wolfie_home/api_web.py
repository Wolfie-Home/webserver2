from flask import Blueprint, request, session

from database.service.location import Location as LocationSvc
from database.service.user import User as UserSvc
from database.service.device import Device as DeviceSvc
from database.service.exceptions import NoRecordError
from wolfie_home.common import request_content_json, login_required_json
from wolfie_home.common import response_json_ok, response_json_error

webapi = Blueprint('web_api', __name__, template_folder='templates')


@webapi.route('/api/login', methods=['POST'])
@request_content_json
def login(content):
    """
    Try login
    """
    import datetime
    try:
        """
        Parameters requirements are here
        """
        username = content.get('username')
        password = content.get("password")
        assert((type(username) is str) and (len(username) < 30))
        assert((type(password) is str) and (len(password) < 30))
    except Exception:
        return response_json_error({}, "Wrong parameter")

    # verify from db
    try:
        user = UserSvc.verify(username, password)
    except NoRecordError as error:
        return response_json_error({}, str(error))  # Usually username password mismatch

    session['username'] = user.username
    session['user_id'] = user.id
    session['email'] = user.email
    session['last_login'] = str(datetime.datetime.now())

    return response_json_ok({'username': user.username,
                             'user_id': user.id}, "Login successful.")


@webapi.route('/api/logout', methods=['POST'])
@login_required_json
def logout():
    """
    Try logout
    """
    try:
        """
        Parameters requirements are here
        """
        pass    # No parameters, only session is required
    except Exception:
        return response_json_error({}, "Wrong parameter")

    # remove the username and id from the session if it's there
    user = session.pop('username', None)
    user_id = session.pop('user_id', None)
    session.pop('last_login', None)
    session.pop('email', None)

    return response_json_ok({'username': user}, "Logout successful.")


@webapi.route('/api/login', methods=['GET'])
@login_required_json
def current_user():
    """
    Get current user session
    """
    # get session
    user = session.get('username', None)
    email = session.get('email', None)
    last_login = session.get('last_login', None)

    return response_json_ok({'username': user, 'email': email, 'last_login': last_login},
                            "User session data successfully returned.")


@webapi.route('/api/location', methods=['GET'])
@login_required_json
def location_list():
    """
    get list of locations
    """
    # session variables required
    user_id = session.get('user_id', None)
    # verify from db
    try:
        locations = LocationSvc.get_list(user_id)
    except NoRecordError as error:
        return response_json_error({}, str(error))  # Usually username password mismatch
    resp = dict()
    resp['locations'] = []
    for obj in locations:
        resp['locations'].append(dict(obj))

    return response_json_ok(resp, "Retrieve locations successful.")


@webapi.route('/api/location/<int:id>', methods=['GET'])
@login_required_json
def location_detail(id):
    """
    get list of locations
    """
    # session variables required
    user_id = session.get('user_id', None)

    try:
        location = LocationSvc.get(user_id, id=id)
    except NoRecordError as error:
        return response_json_error({}, str(error))  # Usually username password mismatch

    try:
        location.rooms = LocationSvc.get_list(user_id, house_id=id)
    except NoRecordError:
        # There is a case of no children rooms
        location.rooms = []

    resp = dict(location)

    return response_json_ok(resp, "Retrieve the location successful.")


@webapi.route('/api/location/<int:id>/device', methods=['GET'])
@login_required_json
def device_list_in_location(id):
    """
    get list of devices
    """
    # session variables required
    user_id = session.get('user_id', None)
    # verify from db
    try:
        devices = DeviceSvc.get_device_list(user_id, location_id=id)
    except NoRecordError as error:
        return response_json_error({}, str(error))  # Usually username password mismatch
    resp = dict()
    resp['devices'] = []
    for obj in devices:
        resp['devices'].append(dict(obj))

    return response_json_ok(resp, "Retrieve devices successful.")


@webapi.route('/api/device', methods=['GET'])
@login_required_json
def device_list():
    """
    get list of devices
    """
    # session variables required
    user_id = session.get('user_id', None)
    # verify from db
    try:
        devices = DeviceSvc.get_device_list(user_id)
    except NoRecordError as error:
        return response_json_error({}, str(error))  # Usually username password mismatch
    resp = dict()
    resp['devices'] = []
    for obj in devices:
        resp['devices'].append(dict(obj))

    return response_json_ok(resp, "Retrieve devices successful.")


@webapi.route('/api/device/<int:id>', methods=['GET'])
@login_required_json
def device_detail(id):
    """
    get list of devices
    """
    # session variables required
    user_id = session.get('user_id', None)
    try:
        # Get devices
        device = DeviceSvc.get_device(user_id, id=id)
    except NoRecordError as error:
        return response_json_error({}, str(error))  # Usually username password mismatch

    try:
        # Get children devices
        device.children = DeviceSvc.get_device_list(user_id, mother_id=id)
    except NoRecordError:
        # There is a case of no children devices
        device.children = []

    resp = dict(device)

    return response_json_ok(resp, "Retrieve devices successful.")


@webapi.route('/api/device/<int:device_id>/parameter', methods=['GET'])
@login_required_json
def parameter_list(device_id):
    """
    get list of parameter of device
    """
    # session variables required
    user_id = session.get('user_id', None)
    # verify from db
    try:
        parameters = DeviceSvc.get_parameter_list(user_id, device_id)
    except NoRecordError as error:
        return response_json_error({}, str(error))  # Usually username password mismatch
    resp = dict()
    resp['parameters'] = []
    for obj in parameters:
        resp['parameters'].append(dict(obj))

    return response_json_ok(resp, "Retrieve parameters successful.")

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
