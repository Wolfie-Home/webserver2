from flask import Blueprint
from flask import render_template

wolfie_home_page = Blueprint('wolfie_home', __name__, template_folder='templates')


@wolfie_home_page.route('/')
def hello_world():
    return render_template('index.html')
