from flask import Blueprint
from flask import render_template
from flask import session

webpage = Blueprint('web_pages', __name__, template_folder='templates')


@webpage.route('/')
@webpage.route('/index')
def main():
    if 'username' in session:
        return render_template('index.html')
    return render_template('login.html')


@webpage.route('/location')
def location():
    if 'username' in session:
        return render_template('location.html')
    return render_template('login.html')