from flask import Blueprint, render_template, session, request, redirect, url_for
from controladores import ControladorCliente
from models import Cliente, Agendamento
from datetime import datetime, timezone
from enums import EnumStatusMensagens, EnumNomesPastaImagem

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
        

@cliente.route('/logout', methods=["GET","POST"])
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
           
    # Instancia o objeto Usuario com os dados do formulário
    cliente = Cliente(
            nome_completo=request.form.get('nome'),
            telefone=telefone_temp,
            cpf=None,
            email=request.form.get('email'),
            senha= request.form.get('senha'),
            foto_nome_usuario= None,
            endereco = None,
            status_usuario=1,
            data_cadastro=datetime.now(timezone.utc),
            data_atualizacao=datetime.now(timezone.utc)
    )
    
    controladorCliente = ControladorCliente() 
    return controladorCliente.cadastrarCliente(cliente)
            
   
@cliente.route('/agendamento/servicos', methods=['GET'])
def clientAgendamentoServicos():
    controladorCliente = ControladorCliente() 
    return controladorCliente.gerenciarAgendamentoServico()

@cliente.route('/agendamento/servicos/cadastro', methods=['POST'])
def clientAgendamentoServicosCadastro():
    dados = request.get_json(silent=True)
    dados_session = session.get('dados_cliente')

    cliente = Cliente(
        id_usuario=dados_session.get('id_cliente'),
        nome_completo=dados_session.get('nome_completo'), 
        telefone=dados_session.get('telefone'), 
        cpf=dados_session.get('cpf'), 
        email=dados_session.get('email'), 
        status_usuario=dados_session.get('status_usuario'), 
        data_cadastro=dados_session.get('data_cadastro'), 
        data_atualizacao=dados_session.get('data_atualizacao')
    )

    agendamento = Agendamento(
        data_agendamento=dados.get('data'),
        hora_inicio=dados.get('horario'),
        hora_fim=dados.get('horario'),
        status_agendamento=True,
        data_atualizacao=datetime.now(),
        servico=None,
        barbeiro=None,
        cliente=cliente
    )
    controladorCliente = ControladorCliente() 
    return controladorCliente.cadastrarAgendamento(agendamento, id_servico = dados.get('id_servico'), id_barbeiro = dados.get('id_barbeiro'))

@cliente.route('/agendamento/meus-agendamentos', methods=['GET'])
def clientMeusAgendamentos():
    controladorCliente = ControladorCliente() 
    return controladorCliente.meusAgendamentos()

@cliente.route('/agendamentos', methods=['GET','POST'])
def clientAgendamento():
   return render_template('pages/cliente/cliente-agendamento-rp.html')

@cliente.route('/cadastro/sucesso', methods=['GET','POST'])
def cadastroSucesso():
   return render_template('pages/cliente/cadastro-realizado-rp.html')

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
    
    
    
    

    

