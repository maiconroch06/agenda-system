from flask import Blueprint, render_template, session, request, redirect, url_for
from controladores import ControladorCliente
from models import Cliente
from datetime import datetime, timezone
from enums import EnumStatusMensagens

cliente = Blueprint('cliente', __name__, template_folder='templates')



@cliente.route('/')
def clientSource():
    #redireciona para a raiz do site novamente
    return redirect('/')
 
@cliente.route('/login', methods=["GET"])
def clientLoginPage():
    return render_template('pages/cliente/cliente-login.html',mensagens_status=EnumStatusMensagens)

@cliente.route('/login', methods=["POST"])
def clientLogin():   
    # Verificando o tipo de request POST
   if request.method == "POST":
        email_digitado = request.form.get('email')
        senha_digitada = request.form.get('senha')
        
        controladorCliente = ControladorCliente()

        return controladorCliente.login(email_digitado,senha_digitada)
        

@cliente.route('/logout', methods=["GET","POSt"])
def logout():
    session.clear()
    return redirect('/')    

@cliente.route('/cadastro', methods=["GET"])
def clientRegisterPage():  
    if session.get("dados_cliente") is None:
        return render_template('pages/cliente/cliente-cadastro.html',mensagens_status=EnumStatusMensagens)
    
    return redirect(url_for('cliente.clientAgendamentoServicos'))
   
@cliente.route('/cadastro', methods=["POST"])
def clientRegister():
        
    #remove a pontuação do telefone      
    telefone_temp = ''.join(filter(str.isdigit,request.form.get('telefone')))
    fotoTemp = request.files.get('foto' , None) 
       
    # Instancia o objeto Usuario com os dados do formulário
    cliente = Cliente(
            nome_completo=request.form.get('nome'),
            telefone=telefone_temp,
            cpf=None,
            email=request.form.get('email'),
            senha= request.form.get('senha'),
            foto_nome= None,
            endereco = None,
            status_usuario=1,
            data_cadastro=datetime.now(timezone.utc),
            data_atualizacao=datetime.now(timezone.utc)
    )
    
    controladorCliente = ControladorCliente()
    
    return controladorCliente.cadastrarCliente(cliente, fotoTemp)
            
   
@cliente.route('/agendamento/servicos', methods=['GET','POST'])
def clientAgendamentoServicos():
    return render_template('pages/cliente/cliente-agendamento-rp.html')

@cliente.route('/agendamentos', methods=['GET','POST'])
def clientAgendamento():
   return render_template('pages/cliente/cliente-agendamento-rp.html')

@cliente.route('/cadastro/sucesso', methods=['GET','POST'])
def cadastroSucesso():
   return render_template('pages/cliente/cadastro_realizado_rp.html')

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
    
    
    
    

    

