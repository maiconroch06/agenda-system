from flask import Blueprint, render_template, redirect, url_for

user_register = Blueprint('register', __name__, template_folder='templates')

@user_register.route('/')
def homePage():
    return render_template('pages/register/user-register.html')