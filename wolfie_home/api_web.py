from flask import Blueprint
from flask import request, session
from flask import jsonify
from flask import abort
from database.models import User

webapi = Blueprint('web_api', __name__, template_folder='templates')


@webapi.route('/api/login', methods=['POST'])
def login():
    # for debugging
    print(request.headers)
    print(request.get_data())

    data = request.form
    print(data)
    user = User.login(request.form['username'], request.form['password'])
    if user.username != request.form['username']:
        abort(400)
    session['username'] = request.form['username']
    return jsonify(**{'username': user.username})
