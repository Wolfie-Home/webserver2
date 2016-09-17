from flask import Blueprint, request, session
from wolfie_home.common import response_json_ok, response_json_error

from database.models import User
from database.service.exceptions import NoRecordError

webapi = Blueprint('web_api', __name__, template_folder='templates')


@webapi.route('/api/login', methods=['POST'])
def login():
    """
    Try login
    """
    content = request.get_json()
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
        user = User.verify(username, password)
    except NoRecordError as error:
        return response_json_error({}, str(error))  # Usually username password mismatch

    session['username'] = user.username
    session['user_id'] = user.id

    return response_json_ok({'username': user.username,
                             'user_id': user.id}, "Login successful.")


@webapi.route('/api/logout', methods=['POST'])
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
    user_id = session.pop('user_idx', None)

    return response_json_ok({'username': user}, "Logout successful.")


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
