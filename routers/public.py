from flask import Blueprint, render_template

publics = Blueprint('public', __name__)

@publics.route('/')
def homePage():
    return render_template('index.html')

@publics.route('/barber')
def registerBarber():
    return render_template('registerBarber.html')