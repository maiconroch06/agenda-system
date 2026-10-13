from flask import Blueprint, render_template
from models.servicos import Servicos
publics = Blueprint('public', __name__)

@publics.route('/')
def homePage():
    servicos = Servicos.consultarTodosOsServicos()
    return render_template('index.html', servicos=servicos)

@publics.route('/tipo-usuario')
def category():
    return render_template('categoria-gestor-barbeiro.html')