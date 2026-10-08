import base64, os
from flask import Blueprint, render_template, redirect, url_for, session, request
from controllers.autenticador_gestor_controller import AutenticadorGestor
from controllers.validar_cadastro_barbeiro import ValidarBarbeiro
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
@gestor.route('/painel/barbeiros', methods=['GET'])
def gestorAbaBarbeiros():
    return render_template('pages/gestor/gestor-gerenciar-barbeiro-rp.html')

    
# Gerenciar Barbeiro (Cadastro) - Cadastro de Barbeiro
# @gestor.route('painel/barbeiro/cadastro', methods=['GET'])
# def gestorBarbeiroCadastro():
#     return render_template('pages/gestor/gestor-barbeiro-rp.html')


# Gerenciar Barbeiro (Cadastro->Validação) - Validando dados informados no cadastro do Barbeiro
@gestor.route('painel/barbeiro/cadastro', methods=['POST'])
def gestorBarbeiroValidar():
    # foto_base64 = foto = request.files.get("foto")

    # # Deve salvar arquivo
    # if foto_base64:
    #     # 1. Isola os dados binários reais da string Base64
    #     if "," in foto_base64:
    #         cabecalho, dados_imagem = foto_base64.split(",", 1)
    #     else:
    #         dados_imagem = foto_base64
            
    #     try:
    #         # 2. Decodifica os bytes da imagem
    #         conteudo_binario = base64.b64decode(dados_imagem)
            
    #         # 3. Garante que as pastas de destino existam para não dar erro de "Folder not found"
    #         pasta_destino = "static/uploads"
    #         os.makedirs(pasta_destino, exist_ok=True)
            
    #         # Remove caracteres especiais do CPF para o nome do arquivo (opcional, mas recomendado)
    #         cpf_limpo = "".join(filter(str.isdigit, cpf)) if cpf else "sem_cpf"
    #         caminho_arquivo = os.path.join(pasta_destino, f"{cpf_limpo}.jpg")
            
    #         # 4. Salva o arquivo final
    #         with open(caminho_arquivo, "wb") as f:
    #             f.write(conteudo_binario)
                
    #     except Exception as e:
    #         # Se a string base64 vier corrompida ou houver erro de permissão de escrita
    #         print(f"Erro ao processar e salvar a imagem: {e}")
    #         # Aqui você pode decidir se retorna um erro para o usuário ou se continua sem foto

    # cpf = request.form.get("cpf")
    # nome = request.form.get("nome")
    # email = request.form.get("email")
    # telefone = request.form.get("telefone")
    # senha = request.form.get("senha")
    # confirmaSenha = request.form.get("confirmar-senha")
    # descricao = request.form.get("descricao")

    # cep = request.form.get("cep")
    # cidade = request.form.get("cidade")
    # uf = request.form.get("unidade-federal")
    # bairro = request.form.get("bairro")
    # logradouro = request.form.get("logradouro")
    # numero = request.form.get("numero")
    # complemento = request.form.get("complemento")
    # sequencia = request.form.get("sequencia")
    return ValidarBarbeiro.validarFormulario(
        request,
        'pages/gestor/gestor-gerenciar-barbeiro-rp.html',
        'gestor.gestorAbaBarbeiros'
    )


# # Gerenciar Barbeiro (Edição) - Editando dados de um Barbeiro existente
# @gestor.route('/editar/barbeiro')
# def gestorBarbeiroEditar():
#     return render_template('pages/gestor/gestor-barbeiro-rp.html')


# Painel Gestor - Aba de Clientes
@gestor.route('/painel/clientes')
def gestorExibirClientes():
    usuario = Cliente()
    return render_template('pages/gestor/gestor-painel-clientes-rp.html', usuarios=usuario.buscarTodosCLientes())

