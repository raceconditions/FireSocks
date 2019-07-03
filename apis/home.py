from flask import render_template, Blueprint

home_api = Blueprint('home_api', __name__, template_folder='templates')

@home_api.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

