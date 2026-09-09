from flask import Blueprint, render_template, redirect, url_for

manager = Blueprint('companies', __name__, template_folder='templates')

@manager.route('/')
def managerSource():
    return redirect('/')

@manager.route('/cadastro/barbeiro')
def managerEmployee():
    return render_template('pages/manager/register-barber.html')

@manager.route('/login')
def managerLogin():
    return render_template('pages/manager/manager-login.html')

@manager.route('/painel')
def managerDashBoard():
    return render_template('pages/manager/manager-panel-restrict.html')