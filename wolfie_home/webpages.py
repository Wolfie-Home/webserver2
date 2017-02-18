from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect, url_for
from .common import login_required_redirect

webpage = Blueprint('web_pages', __name__, template_folder='templates')


@webpage.route('/index')
@webpage.route('/')
def main():
    if 'username' in session:
        return render_template('index.html')
    return render_template('login.html')


@webpage.route('/home')
@login_required_redirect
def home():
    # not implemented yet
    return redirect(url_for('web_pages.location'))


@webpage.route('/location')
@login_required_redirect
def location():
    return render_template('location.html')

@webpage.route('/devices')
@login_required_redirect
def devices():
    return render_template('devices.html')   

@webpage.route('/test')
@login_required_redirect
def test():
    return render_template('test.html');
