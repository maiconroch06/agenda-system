from flask import current_app, Blueprint, render_template, redirect, url_for, session, request, flash
from controladores import ControladorGestor, ControladorBarbeiro
from models import Cliente, Servico, Endereco, Barbeiro, HorarioFuncionamento, AgendaMensal, Recesso
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
    email_digitado = request.form.get('gestor-email-2')
    senha_digitada = request.form.get('gestor-password')
    
    return ControladorGestor.login_gestor(email_digitado,senha_digitada)


# Logout Gestor - Encerramento da sessão do Gestor
@gestor.route('/logout', methods=['POST','GET'])
def gestorLogout():
    session.clear()
    return redirect(url_for('gestor.gestorLogin'))


# Painel Gestor - Aba inicial
@gestor.route('/painel', methods=['POST','GET'])
def gestorPainel():
    return ControladorGestor.consultar_agendamentos(1)

# Painel Gestor - Aba de visualização da Agenda de todos os Barbeiros
@gestor.route('/painel/agendamento')
def gestorAbaAgendamento():
    return render_template('pages/gestor/gestor-painel-agendamento-rp.html')

##################################################################################
#  HORARIO_FUNCIONAMENTO

@gestor.route('/painel/horario_funcionamento')
def gestor_horario_funcionamento_barbearia():
    data_atual = datetime.now(timezone.utc).date()
    return render_template('pages/gestor/gestor-painel-agenda-rp.html', data_atual=data_atual, horario_funcionamento = ControladorGestor.consultar_horario_funcionamento(1), agendas = ControladorGestor.consultar_agenda_mensal_barbearia() ,mensagens_status=EnumStatusMensagens)


@gestor.route('/painel/horario_funcionamento/atualizar', methods=['POST'])
def gestor_horario_funcionamento_barbearia_atualizar():
    
    horario_funcionamento = HorarioFuncionamento(
        id_horario=request.form.get("horario_funcionamento_id"),
        horario_abertura= datetime.strptime(request.form.get("horario_abertura"), "%H:%M").time(),
        horario_fechamento=request.form.get("horario_fechamento"),
        horario_inicio_intrajornada=request.form.get("inicio_almoco"),
        horario_fim_intrajornada=request.form.get("fim_almoco"),
        dias_funcionamento=list(map(int, request.form.getlist("dias_funcionamento")))
    )
       
    return ControladorGestor.atualizar_horario_funcionamento_barbearia(horario_funcionamento)

##################################################################################
# RECESSOS DA BARBEARIA

@gestor.route('/painel/recessos/cadastrar', methods=['POST'])
def gestor_recesso_cadastrar():
    
    recesso = Recesso(
        data_inicio_recesso= datetime.strptime(request.form.get("data_inicio_recesso"),  "%Y-%m-%d").date(),
        data_fim_recesso=datetime.strptime(request.form.get("data_fim_recesso"),  "%Y-%m-%d").date(),
        descricao_recesso=request.form.get("descricao_recesso")
    )
     
    return ControladorGestor.cadastrar_recessos_barbearia_por_mes(recesso)

@gestor.route('/painel/recessos', methods=['GET'])
def gestor_recesso_consultar():   
    return render_template('pages/gestor/gestor-painel-recesso-rp.html', recessos = ControladorGestor.consultar_recessos_barbearia_por_mes(), mensagens_status=EnumStatusMensagens)

@gestor.route('/painel/recessos/excluir', methods=['POST'])
def gestor_recesso_excluir():  
    recesso = Recesso(
        id_recesso=request.form.get("recesso-id", type=int),
        descricao_recesso=request.form.get("recesso-descricao")
    ) 
    return ControladorGestor.excluir_recessos_barbearia_por_mes(recesso)

@gestor.route('/painel/recessos/atualizar', methods=['POST'])
def gestor_recesso_atualizar():  
    
    print("DADOS VINDOS DO MODAL: ", request.form.get("id_recesso", type=int))
    
    
    recesso = Recesso(
        id_recesso=request.form.get("id_recesso", type=int),
        data_inicio_recesso= datetime.strptime(request.form.get("data_inicio_recesso"),  "%Y-%m-%d").date(),
        data_fim_recesso=datetime.strptime(request.form.get("data_fim_recesso"),  "%Y-%m-%d").date(),
        descricao_recesso=request.form.get("descricao_recesso")
    ) 
    return ControladorGestor.atualizar_recessos_barbearia(recesso)

     

##################################################################################
# AGENDA MENSAL 

@gestor.route('/painel/agenda_mensal/cadastrar', methods=['POST'])
def gestor_agenda_cadastrar():
    
    agenda_mensal = AgendaMensal(
        data_inicial_mes= datetime.strptime(request.form.get("data_inicio"),  "%Y-%m-%d").date(),
        data_final_mes=datetime.strptime(request.form.get("data_fim"),  "%Y-%m-%d").date(),
        titulo_agenda=request.form.get("titulo_agenda"), 
    )
     
    return ControladorGestor.cadastrar_agenda_mensal_barbearia(agenda_mensal)

@gestor.route('/painel/agenda_mensal/atualizar', methods=['POST'])
def gestor_agenda_mensal_atualizar():
    
    agenda_mensal = AgendaMensal(
        id_agenda_mensal=request.form.get("agenda_id", type=int),
        data_inicial_mes= datetime.strptime(request.form.get("data_inicio"),  "%Y-%m-%d").date(),
        data_final_mes=datetime.strptime(request.form.get("data_fim"),  "%Y-%m-%d").date(),
        titulo_agenda=request.form.get("titulo_agenda")
    )
     
    return ControladorGestor.atualizar_agenda_mensal_barbearia(agenda_mensal)

@gestor.route('/painel/agenda_mensal/alterar_status', methods=['POST'])
def gestor_agenda_mensal_alterar_status():
        
   
    status_agenda_mensal = request.form.get("agenda-mensal-status", type=int)
   
    agenda_mensal = AgendaMensal(
        
            id_agenda_mensal=request.form.get("agenda-mensal-id", type=int),
            data_inicial_mes= datetime.strptime(request.form.get("data_inicio"),  "%Y-%m-%d").date(),
            data_final_mes=datetime.strptime(request.form.get("data_fim"),  "%Y-%m-%d").date(),
            titulo_agenda=request.form.get("titulo_agenda"),
            status_agenda_mensal= not status_agenda_mensal
    )
    
    return ControladorGestor.atualizar_status_agenda_mensal_barbearia(agenda_mensal)


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
    return render_template('pages/gestor/gestor-painel-barbeiros-rp.html', barbeiros = ControladorBarbeiro.consultar_todos_barbeiros(), mensagens_status=EnumStatusMensagens)


# Gerenciar Barbeiro  - Validando dados informados no cadastro do Barbeiro
@gestor.route('painel/barbeiro/cadastrar', methods=['GET'])
def gestorBarbeiroPage():
    return render_template('pages/gestor/gestor-gerenciar-barbeiro-rp.html', mensagens_status=EnumStatusMensagens)


# Gerenciar Barbeiro (Cadastro->Validação) - Validando dados informados no cadastro do Barbeiro
@gestor.route('painel/barbeiro/cadastrar', methods=['POST'])
def gestor_barbeiro_cadastrar():

    #remove a pontuação do telefone    
  
    telefone_temp = ''.join(filter(str.isdigit,request.form.get('telefone')))
    cep_temp = ''.join(filter(str.isdigit,request.form.get('cep')))
    cpf_temp = ''.join(filter(str.isdigit,request.form.get('cpf')))
    fotoTemp = request.files.get('srv-imagem' , None) 
    agora_utc = datetime.now(timezone.utc)
    
    endereco = Endereco(
        cep=cep_temp,
        cidade=request.form.get('cidade'),
        uf=request.form.get('unidade-federativa'),
        bairro=request.form.get('bairro'),
        logradouro=request.form.get('logradouro'),
        numero=request.form.get('numero'),
        sequencia=request.form.get('sequencia'),
        complemento=request.form.get('complemento')
    )

    # Inicializando o objeto Barbeiro
    barbeiro = Barbeiro(
        id_usuario=None,
        nome_completo=request.form.get('nome'),
        telefone=telefone_temp,
        cpf=cpf_temp,
        email=request.form.get('email'),
        senha=request.form.get('senha'),
        foto_nome_usuario=None,
        status_usuario=True,
        data_cadastro=datetime.now(timezone.utc),
        data_atualizacao=datetime.now(timezone.utc),
        data_liberacao=datetime.now(timezone.utc),
        bio=request.form.get('bio'),
        status_barbeiro=True,
        especialidade=request.form.get('especialidade'),
        data_inicio_carreira=agora_utc.replace(year=agora_utc.year-request.form.get('anos_experiencia', type=int)),   
        endereco=endereco
    )
    
    return ControladorGestor.cadastrarBarbeiro(barbeiro, fotoTemp)


@gestor.route('painel/barbeiro/atualizar', methods=['POST'])
def gestorBarbeiroPageUpdate():
    imagem_form = request.files.get('srv-imagem')
    img_padrao = request.form.get('imagem-padrao', None)
    imagem_anterior = request.form.get('srv-foto_nome_anterior')
    
    cpf_temp = ''.join(filter(str.isdigit,request.form.get('cpf')))
    agora_utc = datetime.now(timezone.utc)
    
     
    barbeiro = Barbeiro(
        id_usuario=request.form.get('srv-id'),
        nome_completo=request.form.get('nome'),
        cpf=cpf_temp,
        telefone=request.form.get('telefone'),
        email=request.form.get('email'),
        senha=request.form.get('senha', None),
        data_atualizacao=datetime.now(timezone.utc),
        status_barbeiro=request.form.get('status_barbeiro', type=int),
        bio=request.form.get('bio'),
        especialidade=request.form.get('especialidade'),
        data_inicio_carreira=agora_utc.replace(year=agora_utc.year-request.form.get('anos_experiencia', type=int))   
    )
        
    return ControladorGestor.atualizar_barbeiro(imagem_form,img_padrao,imagem_anterior, barbeiro)

@gestor.route('painel/barbeiro/endereco/editar', methods=['POST'])
def gestor_barbeiro_editar_endereco():
              
    cep_temp = ''.join(filter(str.isdigit,request.form.get('cep')))
        
    endereco = Endereco(
        id_endereco= request.form.get('bar-end-id'),
        cep=cep_temp,
        cidade=request.form.get('cidade'),
        uf=request.form.get('unidade-federativa'),
        bairro=request.form.get('bairro'),
        logradouro=request.form.get('logradouro'),
        numero=request.form.get('numero'),
        sequencia=request.form.get('sequencia'),
        complemento=request.form.get('complemento')
    )
   
    return ControladorBarbeiro.atualizar_endereco_barbeiro(endereco)


@gestor.route('painel/barbeiro/excluir', methods=['POST'])
def gestor_excluir_barbeiro():
    id_barbeiro = request.form.get('srv-id-deletar')
    foto_nome = request.form.get('srv-foto_nome') 
               
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
    
    if 'dados_barbeiro' in session:
                return redirect(url_for('barbeiro.barbeiroPainel'))
        
    #Criando as rotas publicas para gestor
    routers_publics = ['gestor.gestorSource','gestor.gestorLoginPagina', 'gestor.gestorLogin']
    
    # se a rota for publica ele retorna aqui e envia para a rota desejada;
    if request.endpoint in routers_publics:
        return 
    
    # Se a rota não estiver nas rotas publicas ele verifica q sessão
    if 'dados_gestor' not in session:
        return redirect(url_for('gestor.gestorLoginPagina'))