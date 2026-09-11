from flask import Blueprint, render_template, session, request, redirect, url_for
from sqlalchemy.exc import IntegrityError

from models import User
client = Blueprint('cliente', __name__, template_folder='templates')

@client.route('/')
def clientSource():
    #redireciona para a raiz do site novamente
    return redirect('/')
 
@client.route('/login', methods=["GET", "POST"])
def clientLogin():
    # Verificando o tipo de request GET
    if request.method == "GET":
        return render_template('pages/client/client-login.html')
    
    # Verificando o tipo de request POST
    elif request.method == "POST":
        email_digitado = request.form.get('email')
        senha_digitada = request.form.get('senha')

        # Validação inicial simples
        if not email_digitado or not senha_digitada:
            return render_template('pages/client/client-login.html', erro="Por favor, preencha todos os campos.")

        # 3. Busca o usuário no MySQL através do método que você já criou na sua classe User
        usuario = User.buscar_por_email(email_digitado)

        # 4. Verifica se o usuário existe e se a senha confere
        # (Nota: Se futuramente usar criptografia com werkzeug, use check_password_hash aqui)
        if usuario and usuario.senha_hash == senha_digitada:
            
            # 5. Salva o ID e os dados completos na sessão (Agora incluindo o ID gerado pelo banco!)
            session['dados_usuario'] = usuario.to_dict()
            session['logado'] = True
            
            # Redireciona o cliente logado diretamente para a página de agendamentos
            return clientAgendamentoServicos()
        
        else:
            # Se a senha estiver errada, recarrega mantendo o e-mail na tela
            return render_template(
                'pages/client/client-login.html', 
                erro="E-mail ou senha incorretos.",
                email_antigo=email_digitado
            )
   
@client.route('/cadastro', methods=["GET", "POST"])
def clientRegister():

    # Verificando o tipo de request
    if request.method == "GET":
        # Buscando dados do cliente para alteração
        usuario = session.get("dados_usuario", None)
        return render_template('pages/client/client-register.html')
    
    elif  request.method == "POST":
        # Instancia o objeto User com os dados do formulário
        usuario = User(
            nome=request.form.get('nome'),
            telefone=request.form.get('telefone'),
            email=request.form.get('email'),
            senha=request.form.get('senha'),
            foto=request.files.get('foto').filename if request.files.get('foto') else None
        )
        # Salvando os dados na sessão do Flask
        session['dados_usuario'] = usuario.to_dict()
        return redirect(url_for('cliente.clientRegisterFinish'))

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
   return render_template('pages/client/scheduling.html')

@client.route('/agendamentos', methods=['GET','POST'])
def clientAgendamento():
   return render_template('pages/client/scheduling.html')

