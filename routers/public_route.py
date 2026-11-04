from flask import Blueprint, render_template
from models.servicos import Servicos
from models.barbeiros import Barbeiro

publics = Blueprint('public', __name__)

@publics.route('/')
def homePage():
    barbeiros = Barbeiro.consultarBarbeiros()
    servicos = Servicos.consultarTodosOsServicos()
    return render_template('index.html', servicos=servicos, barbeiros=barbeiros)

@publics.route('/tipo-usuario')
def category():
    return render_template('categoria-gestor-barbeiro.html')