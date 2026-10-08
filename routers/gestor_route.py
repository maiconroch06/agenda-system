from flask import Blueprint, render_template, redirect, url_for, session, request
from controllers.autenticador_gestor_controller import AutenticadorGestor
from models.cliente import Cliente

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

# Autenticação de Gestor - ?
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


# Painel Gestor - Aba de visualização dos Serviços cadastrados
@gestor.route('/painel/servicos')
def gestorAbaServicos():
    return render_template('pages/gestor/gestor-painel-servicos-rp.html')


# Painel Gestor - Aba de visualização dos Barbeiros cadastrados
@gestor.route('/painel', methods=['POST','GET'])
def gestorAbaBarbeiros():
    return render_template('pages/gestor/gestor-painel-barbeiros-rp.html')


    # Gerenciar Barbeiro (Cadastro) - Cadastro de Barbeiro
    @gestor.route('painel/barbeiro/cadastro', methods=['GET'])
    def gestorBarbeiroCadastro():
        return render_template('pages/gestor/gestor-barbeiro-rp.html')


    # Gerenciar Barbeiro (Cadastro->Validação) - Validando dados informados no cadastro do Barbeiro
    @gestor.route('painel/barbeiro/cadastro', methods=['POST'])
    def gestorBarbeiroValidar():
        dados_completos = request.form
        photo = request.form.get("barber-photo")
        cpf = request.form.get("barber-cpf")
        email = request.form.get("barber-email")
        name = request.form.get("barber-name")
        telephone = request.form.get("barber-telephone")
        address = request.form.get("barber-address")
        description = request.form.get("barber-description")
        print(dados_completos)
        return AutenticadorGestor.cadastrarBarbeiro(photo, cpf, name, email, telephone, address, description)


    # Gerenciar Barbeiro (Edição) - Editando dados de um Barbeiro existente
    @gestor.route('/editar/barbeiro')
    def gestorBarbeiroEditar():
        return render_template('pages/gestor/gestor-barbeiro-rp.html')



# Painel Gestor - Aba de Clientes
@gestor.route('/painel/clientes')
def gestorExibirClientes():
    usuario = Cliente()
    return render_template('pages/gestor/gestor-painel-clientes-rp.html', usuarios=usuario.buscarTodosCLientes())

