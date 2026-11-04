from flask import Blueprint, render_template
from models import Servico, Barbeiro

publics = Blueprint('public', __name__)

@publics.route('/')
def homePage():
    barbeiros = ""
    servicos = ""
    return render_template('index.html', servicos=servicos, barbeiros=barbeiros)

@publics.route('/tipo-usuario')
def category():
    return render_template('categoria-gestor-barbeiro.html')