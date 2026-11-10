from flask import Blueprint, render_template
from controladores import ControladorBarbeiro, ControladorServico

publics = Blueprint('public', __name__)

@publics.route('/')
def homePage():
    return render_template('index.html', barbeiros = ControladorBarbeiro.consultar_todos_barbeiros(), servicos = ControladorServico.consultar_servicos_resumido() )

@publics.route('/tipo-usuario')
def category():
    return render_template('categoria-gestor-barbeiro.html')