from flask import Blueprint, render_template, session, request, redirect, url_for
from controllers.authentication_controller import AuthenticationUser
from models import User


client = Blueprint('cliente', __name__, template_folder='templates')

@client.route('/')
def clientSource():
    #redireciona para a raiz do site novamente
    return redirect('/')
 
@client.route('/login', methods=["GET"])
def clientLoginPage():
    # Verificando o tipo de request GET
    if session.get("dados_usuario") is None:
        return render_template('pages/client/client-login.html')
    
    return redirect(url_for('cliente.clientAgendamentoServicos'))

@client.route('/login', methods=["POST"])
def clientLogin():   
    # Verificando o tipo de request POST
   if request.method == "POST":
        email_digitado = request.form.get('email')
        senha_digitada =request.form.get('senha')
        return AuthenticationUser.login(email_digitado,senha_digitada)
        

@client.route('/logout', methods=["GET","POSt"])
def logout():
    session.clear()
    return redirect('/')    

@client.route('/cadastro', methods=["GET"])
def clientRegisterPage():  
    if session.get("dados_usuario") is None:
        return render_template('pages/client/client-register.html')
    
    return redirect(url_for('cliente.clientAgendamentoServicos'))
   
@client.route('/cadastro', methods=["POST"])
def clientRegister():
    if  request.method == "POST":
        # Instancia o objeto User com os dados do formulário
        usuario = User(
            nome_completo=request.form.get('nome'),
            telefone=request.form.get('telefone'),
            email=request.form.get('email'),
            senha= request.form.get('senha'),
            foto=request.files.get('foto').filename if request.files.get('foto') else None,
            id_endereco = None
        )
        return AuthenticationUser.registerUser(usuario)
            
   
@client.route('/agendamento/servicos', methods=['GET','POST'])
def clientAgendamentoServicos():
   return render_template('pages/client/scheduling-rp.html')

@client.route('/agendamentos', methods=['GET','POST'])
def clientAgendamento():
   return render_template('pages/client/scheduling-rp.html')

@client.before_request
def authentication():
    #Criando as minhas rotas publicas
    routers_publics = ['cliente.clientLoginPage','cliente.clientLogin','cliente.clientRegisterPage','cliente.clientRegister']
    
    # se a rota for publica ele retorna aqui e envia para a rota desejada;
    if request.endpoint  in routers_publics:
        return 
    
    # Se a rota não estiver nas rotas publicas ele verifica o token
    if 'dados_usuario' not in session:
        return redirect(url_for('cliente.clientLoginPage'))
    
    
    

    

