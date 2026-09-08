from flask import Blueprint, render_template, session, request,  redirect, url_for
from sqlalchemy.exc import IntegrityError
import requests
from models import User
from datetime import datetime

client = Blueprint('cliente', __name__, template_folder='templates')

@client.route('/')
def clientSource():
    #redireciona para a raiz do site novamente
    return redirect('/')
 
   
@client.route('/cadastro')
def clientRegister():
    return render_template('pages/client/client-register.html')


@client.route('/cadastro/realizar', methods=["POST"])
def clientRegisterUp():

    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    senha = request.form.get('senha')
    tipo_end = request.form.get('tipo_end')

    if not nome or not telefone or not email or not senha:
        return render_template(
            'pages/client/client-register.html',
            erro="Por favor, preencha todos os campos obrigatórios."
        )

    resposta = requests.post(
        'http://localhost:8000/auth/criarContaCliente',
        json={
            "nome_completo": nome,
            "telefone": telefone,
            "email": email,
            "senha": senha,
            "foto": "teste",
            "ativo": 1,
            "data_cadastro": datetime.now().isoformat(),
            "data_atualizacao": datetime.now().isoformat(),
            "endereco_id": 1,
            "cpf": None
        }
    )

    if resposta.status_code == 201:
        return clientAgendamentoServicos()

    dados = resposta.json()

    return render_template(
        'pages/client/client-register.html',
        erro=dados.get(
            'detail',
            'Erro ao realizar cadastro.' # Pegue detail de dados. Se detail não existir, use "Erro ao realizar cadastro." como valor padrão.
        )
    )
   
@client.route('/agendamento/servicos', methods=['GET','POST'])
def clientAgendamentoServicos():
   return render_template('pages/client/scheduling.html')

@client.route('/agendamentos', methods=['GET','POST'])
def clientAgendamento():
   return render_template('pages/client/scheduling.html')


@client.route('/login', methods=["GET", "POST"])
def clientLogin():
    if request.method == "GET":
        return render_template('pages/client/client-login.html')

    email_digitado = request.form.get('email')
    senha_digitada = request.form.get('senha')

    if not email_digitado or not senha_digitada:
        return render_template(
            'pages/client/client-login.html',
            erro="Por favor, preencha todos os campos."
        )

    # Envia login para a API FastAPI
    resposta = requests.post(
        'http://localhost:8000/auth/login',
        json={
            "email": email_digitado,
            "senha": senha_digitada
        }
    )

    # Login realizado com sucesso
    if resposta.status_code == 200:

        dados = resposta.json()

        session['access_token'] = dados['access_token']
        session['dados_usuario'] = dados['usuario']
        session['logado'] = True

        return clientAgendamentoServicos()

    # Erro de autenticação
    return render_template(
        'pages/client/client-login.html',
        erro="E-mail ou senha incorretos.",
        email_antigo=email_digitado
    )
   