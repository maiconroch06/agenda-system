import base64, os
import time
from werkzeug.utils import secure_filename
from flask import current_app, Blueprint, render_template, redirect, url_for, session, request, flash
from controllers.autenticador_gestor_controller import AutenticadorGestor
from models.cliente import Cliente
from models.servicos import Servicos
from models.barbeiros import Barbeiro
from  controllers.validar_cadastro_barbeiro import ValidarBarbeiro
from enums import EnumStatusMensagens
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
        return render_template('pages/gestor/gestor-login.html')
        
    return redirect(url_for('gestor.gestorPainel'))


# Tela de Login - ?
@gestor.route('/login', methods=["POST"])
def gestorLogin():
    email_digitado = request.form.get('manager-email-2')
    senha_digitada = request.form.get('manager-password')
    return AutenticadorGestor.login(email_digitado,senha_digitada)


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
    # consulta no banco, 
    servicos = Servicos().consultarTodosOsServicos()
    return render_template('pages/gestor/gestor-painel-servicos-rp.html', listaServicos = servicos, mensagens_status=EnumStatusMensagens)

# SERVIÇOS - pagina para cadastrar o Serviço
@gestor.route('/painel/servicos/cadastrar', methods=['GET'])
def gestorServicoPageCadastrar():
    return render_template('pages/gestor/gestor-gerenciar-servico-rp.html', mensagens_status=EnumStatusMensagens)

# SERVIÇOS - Rota para enviar o serviço par ao cadastro
@gestor.route('/painel/servicos/cadastrar', methods=['POST'])
def gestorServicoCadastrar():
    
    # validar o tipo de arquivo
    # realizar o up
    # renomeiar com um hash
    imagem = request.files.get('srv-imagem')
    
    foto_nome = 'default.png'
    
    if imagem and imagem.filename:
        # pega a extensao
        extensao = os.path.splitext(imagem.filename)[1]

        # valida a imagem
        if (extensao != '.png' and extensao!='jpg'):
            flash("O sistema só aceita imagens em formato png ou jpg", EnumStatusMensagens.AVISO.value)
            return redirect(url_for('gestor.gestorServicoPageCadastrar'))
     
        foto_nome = f"{int(time.time())}{extensao}"

        # crio o caminho da pasta
        pasta = os.path.join(
            current_app.root_path,
            current_app.config['UPLOAD_FILES'] ,
            'post-imagens') 

        # crio a pasta e caso não exista eu crio automaticamente
        os.makedirs(pasta,exist_ok=True)

        #crio o caminho da pasta com o nome
        caminho = os.path.join(pasta, foto_nome)

        #salvo a imagem no caminho
        imagem.save(caminho)
   
    descricao_servico = request.form.get('srv-nome').strip()
    valor = Decimal(request.form.get('srv-preco').strip())
    duracao = request.form.get('srv-duracao').strip()

     
    return AutenticadorGestor.cadastrarServico(foto_nome, descricao_servico, valor, duracao)

# SERVIÇOS - REMOVER
@gestor.route('/painel/servicos/deletar', methods=['POST'])
def gestorServicoDeletar(): 
    id_servico = request.form.get('srv-id-deletar')
    servico = Servicos()
    servico.consultarIdServico(id_servico)
    
    if servico is None:
        flash("Aviso: Serviço não deletado, serviço inexistente ", EnumStatusMensagens.AVISO.value)
        return redirect(url_for("gestor.gestorAbaServicos"))
    
    return AutenticadorGestor.deletarServico(id_servico)

# SERVIÇOS - Editar servico
@gestor.route('/painel/servicos/editar/<int:id_servico>', methods=['GET'])
def gestorServicoEditarPagina(id_servico:int):

    servico = Servicos().consultarIdServico(id_servico)
            
    if servico is None:
        flash("Edição não efetuado, serviço inexistente", EnumStatusMensagens.AVISO.value)
        return redirect(url_for("gestor.gestorAbaServicos"))
    
    return render_template('pages/gestor/gestor-gerenciar-servico-rp.html', servico = servico, mensagens_status=EnumStatusMensagens)

# SERVIÇOS - Salvar edição do serviço no banco de dados
@gestor.route('/painel/servicos/editar', methods=['POST'])
def gestorServicoEditar():
        
    foto_nome = "foto_nome"
    descricao_servico = request.form.get('srv-nome')
    valor = Decimal(request.form.get('srv-preco').strip())
    duracao = request.form.get('srv-duracao').strip()
    ativo = request.form.get('srv-status', type=int)
    id = request.form.get('srv-id')


    return AutenticadorGestor.editarServico(id, foto_nome, descricao_servico, valor, duracao, ativo)

    

    

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
    
    return ValidarBarbeiro.validarFormulario(
        request,
        'pages/gestor/gestor-gerenciar-barbeiro-rp.html',
        'gestor.gestorAbaBarbeiros',
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