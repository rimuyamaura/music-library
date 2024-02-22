from flask import Blueprint, render_template, session


home_blueprint = Blueprint(
    'home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    session.pop('_flashes', None)
    return render_template('home.html')
