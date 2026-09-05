from flask import Blueprint, render_template, redirect, url_for

gestor = Blueprint('companies', __name__, template_folder='templates')

@gestor.route('/')
def managerDashBoard():
    return 'Aqui vai ficar o dashBoar do gestor'

@gestor.route('/funcionario/cadastro')
def managerEmployee():
    return render_template('registerBarber.html')