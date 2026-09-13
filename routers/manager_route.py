from flask import Blueprint, render_template, redirect, url_for, session, request
from controllers.authentication_manager_controller import AuthenticationManager

manager = Blueprint('gestor', __name__, template_folder='templates')

@manager.route('/')
def managerSource():
    return redirect('/')

@manager.route('/cadastro/barbeiro')
def registerEmployee():
    return render_template('pages/manager/manage-barber-rp.html')

@manager.route('/editar/barbeiro')
def managerEmployee():
    return render_template('pages/manager/manage-barber-rp.html')

@manager.route('/login', methods=['GET'])
def managerLoginPage():
    if session.get('dados_gestor') is None:
        return render_template('pages/manager/manager-login.html')
        
    return redirect(url_for('gestor.managerPanel'))

@manager.route('/login', methods=["POST"])
def managerLogin():
    email_digitado = request.form.get('manager-email-2')
    senha_digitada =request.form.get('manager-password')
    return AuthenticationManager.login(email_digitado,senha_digitada)

@manager.route('/painel', methods=['POST','GET'])
def managerPanel():
    return render_template('pages/manager/manager-panel-rp.html')


@manager.route('/logout', methods=['POST','GET'])
def managerLogout():
    session.clear()
    return redirect('/')



@manager.before_request
def authentication():
    
    #Varifica se o cliente tem sessão
    if 'dados_cliente' in session:
            return redirect(url_for('cliente.clientAgendamentoServicos'))
        
        
    #Criando as minhas rotas publicas
    routers_publics = ['gestor.managerSource','gestor.managerLoginPage', 'gestor.managerLogin']
    
    # se a rota for publica ele retorna aqui e envia para a rota desejada;
    if request.endpoint  in routers_publics:
        return 
    
    # Se a rota não estiver nas rotas publicas ele verifica o token
    
    if 'dados_gestor' not in session:
        return redirect(url_for('gestor.managerLoginPage'))