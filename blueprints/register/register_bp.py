from flask import Blueprint, render_template, redirect, session, url_for, request
import sqlite3
from models.User import User
from models.Address import Endereco

register_bp = Blueprint('register', __name__, template_folder='templates')

@register_bp.route('/')
def userRegister():
    return render_template('view/register/user-register.html')

@register_bp.route('/endereco', methods=['GET', 'POST'])
def adressRegister():

    # Dicionário com os estados
    estado_siglas = {
        "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
        "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
        "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
        "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
        "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins"
    }

    if request.method == 'POST':
        # Instancia o objeto User com os dados do formulário
        novo_usuario = User(
            cpf=request.form.get('cpf'),
            nome=request.form.get('nome'),
            sobrenome=request.form.get('sobrenome'),
            telefone=request.form.get('telefone'),
            email=request.form.get('email'),
            senha=request.form.get('senha'),
            foto=request.files.get('foto').filename if request.files.get('foto') else None
        )

        try:
            # Chama o método de inserção da classe
            novo_usuario.salvar()

            # Salva o CPF do usuário recém-cadastrado na sessão HTTP
            session['usuario_cpf'] = novo_usuario.cpf
            return render_template('register/adress-register.html', estado_siglas=estado_siglas)

        except sqlite3.IntegrityError:
            return "Erro: CPF ou E-mail já cadastrados.", 400
        
    return render_template('register/adress-register.html', estado_siglas=estado_siglas)


@register_bp.route('/finalizacao', methods=['POST'])
def finishRegister():
    # Recupera o CPF que foi guardado na sessão durante a rota anterior
    cpf_usuario = session.get('usuario_cpf')

    # Valida se o CPF existe na sessão antes de tentar cadastrar o endereço
    if not cpf_usuario:
        return "Erro: Sessão expirada ou usuário não identificado.", 400

    # CORREÇÃO: Captura exatamente as propriedades "name" vindas do formulário HTML
    novo_endereco = Endereco(
        cep=request.form.get('end-cep'),
        cidade=request.form.get('end-cidade'),
        estado_sigla=request.form.get('end-estado-sigla'),
        logradouro=request.form.get('end-logradouro'),
        numero=request.form.get('end-numero'),       # Alterado de 'numero' para 'end-numero'
        bairro=request.form.get('end-bairro'),
        sequencia=request.form.get('end-sequencia'),
        complemento=request.form.get('end-complemento'),
        usuario_cpf=cpf_usuario 
    )

    try:
        novo_endereco.salvar()
        return render_template('register/finish-register.html')
    except Exception as e:
        # Exibe o erro real no terminal do Flask para facilitar o seu diagnóstico
        print(f"Erro detalhado no banco de dados: {e}")
        return f"Erro ao salvar o endereço: {e}", 400

@register_bp.route('/tipoUsuario')
def userCategory():
    return render_template('register/user-category-type-panel.html')