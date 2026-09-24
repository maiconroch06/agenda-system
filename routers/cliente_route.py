from flask import Blueprint, render_template, session, request, redirect, url_for
from controllers.autenticador_cliente_controller import AutenticacaoCliente
from models import Usuario


cliente = Blueprint('cliente', __name__, template_folder='templates')

@cliente.route('/')
def clientSource():
    #redireciona para a raiz do site novamente
    return redirect('/')
 
@cliente.route('/login', methods=["GET"])
def clientLoginPage():
    # Verificando o tipo de request GET
    if session.get("dados_cliente") is None:
        return render_template('pages/client/client-login.html')
    
    return redirect(url_for('cliente.clientAgendamentoServicos'))

@cliente.route('/login', methods=["POST"])
def clientLogin():   
    # Verificando o tipo de request POST
   if request.method == "POST":
        email_digitado = request.form.get('email')
        senha_digitada =request.form.get('senha')
        return AutenticacaoCliente.login(email_digitado,senha_digitada)
        

@cliente.route('/logout', methods=["GET","POSt"])
def logout():
    session.clear()
    return redirect('/')    

@cliente.route('/cadastro', methods=["GET"])
def clientRegisterPage():  
    if session.get("dados_cliente") is None:
        return render_template('pages/client/client-register.html')
    
    return redirect(url_for('cliente.clientAgendamentoServicos'))
   
@cliente.route('/cadastro', methods=["POST"])
def clientRegister():
    if  request.method == "POST":
        #COLOCAR A VALIDAÇÃO AQUI
              
        telefone_temp = ''.join(filter(str.isdigit,request.form.get('telefone')))
        # Instancia o objeto Usuario com os dados do formulário
        usuario = Usuario(
            nome_completo=request.form.get('nome'),
            telefone=telefone_temp,
            email=request.form.get('email'),
            senha= request.form.get('senha'),
            foto=request.files.get('foto').filename if request.files.get('foto') else None,
            id_endereco = None
        )
        return AutenticacaoCliente.registrarCliente(usuario)
            
   
@cliente.route('/agendamento/servicos', methods=['GET','POST'])
def clientAgendamentoServicos():
   return render_template('pages/client/scheduling-rp.html')

@cliente.route('/agendamentos', methods=['GET','POST'])
def clientAgendamento():
   return render_template('pages/client/scheduling-rp.html')

@cliente.before_request
def authentication():
    
    if 'dados_gestor' in session:
        return redirect(url_for('gestor.managerPanel'))
        
        
    #Criando as minhas rotas publicas
    routers_publics = ['cliente.clientLoginPage','cliente.clientLogin','cliente.clientRegisterPage','cliente.clientRegister']
    
    # se a rota for publica ele retorna aqui e envia para a rota desejada;
    if request.endpoint  in routers_publics:
        return 
    
    # Se a rota não estiver nas rotas publicas ele verifica a sessão
    # Caso o usuario tente acessar uma rota privada ele redireciona para uma rota publica
    if 'dados_cliente' not in session:
        return redirect(url_for('cliente.clientLoginPage'))
    
    
    
    

    

