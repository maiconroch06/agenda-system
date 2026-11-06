from flask import current_app, Blueprint, render_template, redirect, url_for, session, request, flash
from controladores.controlador_gestor import ControladorGestor
from models.cliente import Cliente
from models.servicos import Servico
from models.barbeiros import Barbeiro
from  controladores import ControladorBarbeiro
from enums import EnumStatusMensagens, EnumNomesPastaImagem
from decimal import Decimal


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
    
    return ControladorGestor.login(email_digitado,senha_digitada)


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
@gestor.route('/painel/servicos/deletar', methods=['POST'])
def gestor_excluir_servico(): 
    id_servico = request.form.get('srv-id-deletar')   
    return ControladorGestor.deletarServico(id_servico)
  

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
    barbeiros = Barbeiro()
    return render_template('pages/gestor/gestor-painel-barbeiros-rp.html', barbeiros = barbeiros.consultarBarbeiros(), mensagens_status=EnumStatusMensagens)


# Gerenciar Barbeiro  - Validando dados informados no cadastro do Barbeiro
@gestor.route('painel/barbeiro/cadastrar', methods=['GET'])
def gestorBarbeiroPage():
    return render_template('pages/gestor/gestor-gerenciar-barbeiro-rp.html', mensagens_status=EnumStatusMensagens)


# Gerenciar Barbeiro (Cadastro->Validação) - Validando dados informados no cadastro do Barbeiro
@gestor.route('painel/barbeiro/cadastrar', methods=['POST'])
def gestorBarbeiroValidar():

    imagem = request.files.get('foto')

    enviarImagem = ValidadorDeImagens() 
    foto_nome = enviarImagem.enviarImagem(imagem, EnumNomesPastaImagem.IMAGENS_BARBEIRO)

    if foto_nome is None:
            flash("Atenção: a imagem não é suportada pelo sistema.", EnumStatusMensagens.AVISO.value)
            return redirect(url_for('gestor.gestorServicoEditarPagina'))
    
    return ValidarBarbeiro.validarFormularioCriarEditarBarbeiro(
        request,
        'pages/gestor/gestor-gerenciar-barbeiro-rp.html',
        'gestor.gestorAbaBarbeiros',
        id_barbeiro = None
    )

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



##################################################################################
#  CLIENTES
@gestor.route('/painel/clientes')
def gestorExibirClientes():
    usuario = Cliente()
    return render_template('pages/gestor/gestor-painel-clientes-rp.html', usuarios=usuario.buscarTodosCLientes())

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