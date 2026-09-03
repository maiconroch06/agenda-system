import sqlite3
from flask import Blueprint, render_template, redirect, url_for, request, session

from models import User
from models import Address
from repository import obter_todos_estados

user_register = Blueprint('register', __name__, template_folder='templates')

@user_register.route('/', methods=['GET'])
def register_User_get():
    return render_template('pages/register/user-register.html')

@user_register.route('/', methods=['POST'])
def register_User_post():

    # Dados da sessão do usuário, se houver
    session_usr = session.get('dados-usuario', None)
    
    # Instancia o objeto User com os dados do formulário
    usuario = User(
        cpf=request.form.get('cpf'),
        nome=request.form.get('nome'),
        sobrenome=request.form.get('sobrenome'),
        telefone=request.form.get('telefone'),
        email=request.form.get('email'),
        senha=request.form.get('senha'),
        foto=request.files.get('foto').filename if request.files.get('foto') else None
    )

    try:
        if session_usr:

            if(usuario.cpf == session_usr.get('cpf')):
                # Atualiza os dados do usuário existente no banco de dados
                usuario.atualizar()
            else:
                # Se o CPF mudou, atualiza a sessão com os novos dados e deleta o antigo
                usuario.excluir_por_cpf(session_usr.get('cpf'))
                usuario.salvar()
            
        else:
            # Chama o método de inserção da classe
            usuario.salvar()

        # Salva os dados na sessão para correção do cliente
        session['dados-usuario'] = usuario.to_dict()
        return register_Address_get()
        
    except sqlite3.IntegrityError:
        return "Erro: CPF ou E-mail já cadastrados.", 400

@user_register.route('/endereco', methods=['GET'])
def register_Address_get():
    estado_siglas = obter_todos_estados()
    return render_template('pages/register/address-register.html', estado_siglas=estado_siglas)

@user_register.route('/endereco', methods=['POST'])
def register_Address_post():

    session_addr = session.get('dados-endereco', None)

    # Recupera o CPF que foi guardado na sessão durante a rota anterior
    cpf_usuario = session.get('dados-usuario', {}).get('cpf')

    # Valida se o CPF existe na sessão antes de tentar cadastrar o endereço
    if not cpf_usuario:
        return "Erro: Sessão expirada ou usuário não identificado.", 400

    # CORREÇÃO: Captura exatamente as propriedades "name" vindas do formulário HTML
    endereco = Address(
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
        # Se já existia um endereço iniciado nesta sessão
        if session_addr:
            sequencia_antiga = session_addr.get('sequencia')

            # Se a sequência continua igual, basta atualizar as outras colunas
            if sequencia_antiga == endereco.sequencia:
                endereco.atualizar()
            
            # Se a sequência mudou, precisamos deletar o registro antigo (com a pk antiga) e salvar o novo
            else:
                Address.excluir_por_cpf_e_sequencia(cpf_usuario, sequencia_antiga)
                endereco.salvar()
        else:
            # Se for a primeiríssima vez enviando o endereço, apenas salva
            endereco.salvar()

        # Salva os dados na sessão para correção do cliente
        session['dados-endereco'] = endereco.to_dict()

        return finish_Register()
    
    except Exception as e:
        # Exibe o erro real no terminal do Flask para facilitar o seu diagnóstico
        print(f"Erro detalhado no banco de dados: {e}")
        return f"Erro ao salvar o endereço: {e}", 400

@user_register.route('/finalizacao', methods=['GET'])
def finish_Register():
    return render_template('pages/register/finish-register.html')

@user_register.route('/usuario-categoria', methods=['GET'])
def user_category():
    session.pop('dados-usuario', None)  # Limpa os dados do usuário da sessão
    session.pop('dados-endereco', None)  # Limpa os dados do endereço da sessão
    return render_template('pages/register/user-category-type-panel.html')