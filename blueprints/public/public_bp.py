from flask import Blueprint, render_template, redirect, url_for

public_bp = Blueprint('public', __name__, template_folder='templates')

@public_bp.route('/')
def homePage():
    return render_template('public/index.html')