from flask import Blueprint, render_template, redirect, url_for, session, request
from controladores import ControladorBarbeiro
from enums import EnumStatusMensagens

barbeiro = Blueprint('barbeiro', __name__, template_folder='templates')

@barbeiro.route('/')
def barberSource():
    return redirect('/')

##################################################################################
# Logout Barbeiro - Encerramento da sessão do Barbeiro

@barbeiro.route('/logout', methods=['POST','GET'])
def barbeiroLogout():
    session.clear()
    return redirect('/')

##################################################################################
# Acesso do Barbeiro - Criação da sessão

@barbeiro.route('/login', methods=["POST"])
def barbeiroLogin():
    email_digitado = request.form.get('barbeiro-email-2')
    senha_digitada = request.form.get('barbeiro-password')
    
    return ControladorBarbeiro.login_barbeiro(email_digitado,senha_digitada)

##################################################################################
# O que isso esta fazendo? A mesma função existe no gestor

@barbeiro.route('/login')
def barbeiroLoginPagina():
    if session.get('dados_barbeiro') is None:
        return render_template('pages/barbeiro/barbeiro-login.html', mensagens_status=EnumStatusMensagens)
        
    return redirect(url_for('barbeiro.barbeiroPainel'))

##################################################################################
# Painel de Visualização de Agendamentos

@barbeiro.route('/painel')
def barbeiroPainel():
    barbeiro = session.get('dados_barbeiro')

    agendamentos_flask = ControladorBarbeiro.consultar_agendamentos_barbeiro(barbeiro)
    
    #print("\n 1. BARBEIRO NA SESSÃO: ", barbeiro)
    #print("\n 2. AGENDAMENTOS RETORNADOS: ", agendamentos_flask)

    return render_template('pages/barbeiro/barbeiro-painel-inicio-rp.html', barbeiro=barbeiro, agendamentos_flask=agendamentos_flask)
