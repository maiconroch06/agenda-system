from flask import Blueprint, render_template, redirect, url_for, session, request
from controllers.autenticador_gestor_controller import AutenticadorGestor

gestor = Blueprint('gestor', __name__, template_folder='templates')

@gestor.route('/')
def managerSource():
    return redirect('/')

@gestor.route('/cadastro/barbeiro', methods=['GET'])
def registerEmployee():
    return render_template('pages/manager/manage-barber-rp.html')

@gestor.route('/cadastro/barbeiro', methods=['POST'])
def validateEmployee():
    photo = request.form.get("barber-photo")
    cpf = request.form.get("barber-cpf")
    email = request.form.get("barber-email")
    name = request.form.get("barber-name")
    telephone = request.form.get("barber-telephone")
    address = request.form.get("barber-address")
    description = request.form.get("barber-description")
    return AutenticadorGestor.cadastrarBarbeiro(photo, cpf, name, email, telephone, address, description)

@gestor.route('/editar/barbeiro')
def managerEmployee():
    return render_template('pages/manager/manage-barber-rp.html')

@gestor.route('/login', methods=['GET'])
def managerLoginPage():
    if session.get('dados_gestor') is None:
        return render_template('pages/manager/manager-login.html')
        
    return redirect(url_for('gestor.managerPanel'))

@gestor.route('/login', methods=["POST"])
def managerLogin():
    email_digitado = request.form.get('manager-email-2')
    senha_digitada =request.form.get('manager-password')
    return AutenticadorGestor.login(email_digitado,senha_digitada)

@gestor.route('/painel', methods=['POST','GET'])
def managerPanel():
    return render_template('pages/manager/manager-panel-rp.html')


@gestor.route('/logout', methods=['POST','GET'])
def managerLogout():
    session.clear()
    return redirect('/')



@gestor.before_request
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