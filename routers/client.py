from flask import Blueprint, render_template, session, request, redirect, url_for
from sqlalchemy.exc import IntegrityError
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
        return render_template('pages/client/client-login.html')


@client.route('/login/', methods=["POST"])
def clientLogin():   
    # Verificando o tipo de request POST
   if request.method == "POST":
        email_digitado = request.form.get('email')
        senha_digitada = request.form.get('senha')
        return AuthenticationUser.login(email_digitado,senha_digitada)
        

@client.route('/cadastro', methods=["GET"])
def clientRegisterPage():  
    usuario = session.get("dados_usuario", None)
    return render_template('pages/client/client-register.html')
   
@client.route('/cadastro', methods=["POST"])
def clientRegister():
    if  request.method == "POST":
        # Instancia o objeto User com os dados do formulário
        usuario = User(
            nome_completo=request.form.get('nome'),
            telefone=request.form.get('telefone'),
            email=request.form.get('email'),
            senha=request.form.get('senha'),
            foto=request.files.get('foto').filename if request.files.get('foto') else None,
            id_endereco = None
        )
        return AuthenticationUser.registerUser(usuario)
    
    

@client.route('/cadastro/finalizacao', methods=["GET", "POST"])
def clientRegisterFinish():
    # Buscando dados do usuário da sessão
    usuario = session.get("dados_usuario")

    # Se tentar acessar a URL direto sem preencher o primeiro formulário, joga para o início do cadastro.
    if not usuario:
        return render_template('pages/client/client-register.html')
    
    # Verificando o tipo de request
    if request.method == "GET":
        print("Teste")
        return render_template('pages/client/finish-register.html')
    
    elif request.method == "POST":
        try:
            # 4. Reconstrói o objeto User a partir dos dados da sessão
            usuario_final = User(
                nome=usuario['nome'],
                telefone=usuario['telefone'],
                email=usuario['email'],
                senha=usuario['senha'], 
                foto=usuario['foto_path']
            )
            # 6. SALVA AMBOS NO BANCO DE DADOS (MySQL)
            usuario_final.salvar()
            
            session['dados_usuario'] = usuario_final.to_dict()
            session['logado'] = True
            return clientAgendamentoServicos()
        
        except IntegrityError:
            # 🔥 CAPTURA ERRO DE DUPLICIDADE: Se o e-mail já existir, cai aqui.
            # Recarregamos a página de finalização passando uma mensagem de erro estilizada.
            return render_template(
                'pages/client/client-register.html', 
                erro="Este e-mail já está cadastrado no sistema. Por favor, utilize outro."
            )
        
        except Exception as e:
            return f"Erro ao salvar no banco de dados: {str(e)}", 400
        
   
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
    
    
    

    

