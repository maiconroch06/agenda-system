from flask import Blueprint, render_template, redirect, url_for

register_bp = Blueprint('register', __name__, template_folder='templates')

@register_bp.route('/')
def userRegister():
    return render_template('register/user-register.html')

@register_bp.route('/endereço')
def adressRegister():
    return render_template('register/adress-register.html')

@register_bp.route('/finalizacao')
def finishRegister():
    return render_template('register/finish-register.html')

@register_bp.route('/tipoUsuario')
def userCategory():
    return render_template('register/user-category-type-panel.html')