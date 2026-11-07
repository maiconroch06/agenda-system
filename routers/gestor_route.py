from flask import current_app, Blueprint, render_template, redirect, url_for, session, request, flash
from controladores import ControladorGestor, ControladorBarbeiro
from models import Cliente, Servico, Endereco, Barbeiro
from enums import EnumStatusMensagens, EnumNomesPastaImagem
from decimal import Decimal
from datetime import datetime, timezone


gestor = Blueprint('gestor', __name__, template_folder='templates')

# Rota de redirecionamento a Home Page
@gestor.route('/')
def gestorSource():
    return redirect('/')


# Tela de Login (Utilitário+Tela) - Preenchimento de dados já cadastrados no banco do Gestor
@gestor.route('/login', methods=['GET'])
def gestorLoginPagina():
    if session.get('dados_gestor') is None:
        return render_template('pages/gestor/gestor-login.html', mensagens_status=EnumStatusMensagens)
        
    return redirect(url_for('gestor.gestorPainel'))


# Envio dos dados a partid da Tela de Login
@gestor.route('/login', methods=["POST"])
def gestorLogin():
    email_digitado = request.form.get('manager-email-2')
    senha_digitada = request.form.get('manager-password')
    
    return ControladorGestor.login_gestor(email_digitado,senha_digitada)


# Logout Gestor - Encerramento da sessão do Gestor
@gestor.route('/logout', methods=['POST','GET'])
def gestorLogout():
    session.clear()
    return redirect('/')


# Painel Gestor - Aba inicial
@gestor.route('/painel', methods=['POST','GET'])
def gestorPainel():
    return render_template('pages/gestor/gestor-painel-inicio-rp.html')


# Painel Gestor - Aba de visualização da Agenda de todos os Barbeiros
@gestor.route('/painel/agenda')
def gestorAbaAgenda():
    return render_template('pages/gestor/gestor-painel-agenda-rp.html')

##################################################################################
# SERVIÇOS - Aba de visualização de todos Serviços cadastrados
@gestor.route('/painel/servicos')
def gestorAbaServicos():     
    return ControladorGestor.consultar_servicos()

# SERVIÇOS - pagina para cadastrar o Serviço
@gestor.route('/painel/servicos/cadastrar', methods=['GET'])
def gestorServicoPageCadastrar():
    return render_template('pages/gestor/gestor-gerenciar-servico-rp.html', mensagens_status=EnumStatusMensagens)

# SERVIÇOS - Rota para enviar o serviço par ao cadastro
@gestor.route('/painel/servicos/cadastrar', methods=['POST'])
def gestorServicoCadastrar():
    
    imagem = request.files.get('srv-imagem')
    
    descricao_servico = request.form.get('srv-descricao-servico').strip()
    valor = request.form.get('srv-valor').strip()
    duracao = request.form.get('srv-duracao').strip()
         
    return ControladorGestor.cadastrarServico(imagem, descricao_servico, valor, duracao)

# SERVIÇOS - REMOVER
@gestor.route('/painel/servicos/excluir', methods=['POST'])
def gestor_excluir_servico(): 
    id_servico = request.form.get('srv-id-deletar')
    foto_nome = request.form.get('srv-foto_nome') 
    
    return ControladorGestor.excluir_servico(id_servico, foto_nome)
  

# SERVIÇOS - Salvar edição do serviço no banco de dados
@gestor.route('/painel/servicos/editar', methods=['POST'])
def gestorServicoEditar():

    imagem_form = request.files.get('srv-imagem')
    img_padrao = request.form.get('imagem-padrao', None)
    imagem_anterior = request.form.get('srv-foto_nome_anterior')
  
    descricao_servico = request.form.get('srv-descricao-servico')
    valor = request.form.get('srv-valor').strip()
    duracao = request.form.get('srv-duracao').strip()
    ativo = request.form.get('srv-status', type=int)
    id = request.form.get('srv-id')
  
    return ControladorGestor.editarServico(id, imagem_form, img_padrao, imagem_anterior, descricao_servico, valor, duracao, ativo)


##################################################################################
# BARBEIROS - Aba de visualização dos Barbeiros cadastrados
@gestor.route('/painel/barbeiros', methods=['GET'])
def gestorAbaBarbeiros():
    return ControladorBarbeiro.consultar_todos_barbeiros()


# Gerenciar Barbeiro  - Validando dados informados no cadastro do Barbeiro
@gestor.route('painel/barbeiro/cadastrar', methods=['GET'])
def gestorBarbeiroPage():
    return render_template('pages/gestor/gestor-gerenciar-barbeiro-rp.html', mensagens_status=EnumStatusMensagens)


# Gerenciar Barbeiro (Cadastro->Validação) - Validando dados informados no cadastro do Barbeiro
@gestor.route('painel/barbeiro/cadastrar', methods=['POST'])
def gestorBarbeiroValidar():

    #remove a pontuação do telefone    
  
    telefone_temp = ''.join(filter(str.isdigit,request.form.get('telefone')))
    cep_temp = ''.join(filter(str.isdigit,request.form.get('cep')))
    cpf_temp = ''.join(filter(str.isdigit,request.form.get('cpf')))
    fotoTemp = request.files.get('srv-imagem' , None) 

    endereco = Endereco(
        cep=cep_temp,
        cidade=request.form.get('cidade'),
        estados_br_sigla=request.form.get('unidade-federativa'),
        bairro=request.form.get('bairro'),
        logradouro=request.form.get('logradouro'),
        numero=request.form.get('numero'),
        sequencia=request.form.get('sequencia'),
        complemento=request.form.get('complemento')
    )

    # Inicializando o objeto Barbeiro
    barbeiro = Barbeiro(
        id=None,
        nome_completo=request.form.get('nome'),
        telefone=telefone_temp,
        cpf=cpf_temp,
        email=request.form.get('email'),
        senha=request.form.get('senha'),
        foto_nome=None,
        status_usuario=True,
        data_cadastro=datetime.now(timezone.utc),
        data_atualizacao=datetime.now(timezone.utc),
        data_liberacao=datetime.now(timezone.utc),
        descricao=request.form.get('descricao'),
        status_barbeiro=True,
        endereco=endereco
    )
    
    return ControladorGestor.cadastrarBarbeiro(barbeiro, fotoTemp)

@gestor.route('painel/barbeiro/editar/<int:id_barbeiro>', methods=['GET'])
def gestorBarbeiroPageEdit(id_barbeiro:int):
    barbeiro = Barbeiro().consultarIdBarbeiro(id_barbeiro)

    # return f"Dados barbeiro: {barbeiro}"
    return render_template('pages/gestor/gestor-gerenciar-barbeiro-rp.html', barbeiro = barbeiro, mensagens_status=EnumStatusMensagens)

@gestor.route('painel/barbeiro/atualizar/<int:id_barbeiro>', methods=['POST'])
def gestorBarbeiroPageUpdate(id_barbeiro:int):

    return ValidarBarbeiro.validarFormulario(
            request,
            'pages/gestor/gestor-gerenciar-barbeiro-rp.html',
            'gestor.gestorAbaBarbeiros',
            id_barbeiro = id_barbeiro
        )


@gestor.route('painel/barbeiro/excluir', methods=['POST'])
def gestor_excluir_barbeiro():
    id_barbeiro = request.form.get('srv-id-deletar')
    foto_nome = request.form.get('srv-foto_nome') 
    
    print(foto_nome)
        
    return ControladorGestor.excluir_barbeiro(id_barbeiro, foto_nome)

    



##################################################################################
#  CLIENTES
@gestor.route('/painel/clientes')
def gestorExibirClientes():
    return ControladorGestor.consultar_clientes()

##################################################################################
# FINANCEIRO
@gestor.route('/painel/financeiro')
def gestorPainelFinaceiro():
    return render_template('pages/gestor/gestor-painel-financeiro-rp.html')

##################################################################################
# CONFIGURAÇÃO DAS ROTAS PRIVADAS
@gestor.before_request
def authentication():
    #Varifica se o cliente tem sessão
    if 'dados_cliente' in session:
            return redirect(url_for('cliente.clientAgendamentoServicos'))
        
    #Criando as rotas publicas para gestor
    routers_publics = ['gestor.gestorSource','gestor.gestorLoginPagina', 'gestor.gestorLogin']
    
    # se a rota for publica ele retorna aqui e envia para a rota desejada;
    if request.endpoint in routers_publics:
        return 
    
    # Se a rota não estiver nas rotas publicas ele verifica q sessão
    if 'dados_gestor' not in session:
        return redirect(url_for('gestor.gestorLoginPagina'))