from flask import Blueprint, render_template, redirect, url_for

manager = Blueprint('companies', __name__, template_folder='templates')

@manager.route('/')
def managerDashBoard():
    return 'Aqui vai ficar o dashBoar do gestor'

@manager.route('/funcionario/cadastro')
def managerEmployee():
    return render_template('registerBarber.html')

@manager.route('/login')
def managerLogin():
    return render_template('pages/manager/manager-login.html')