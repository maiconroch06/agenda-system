from flask import current_app, Blueprint, render_template, redirect, url_for, session, request, flash
from controladores import ControladorGestor, ControladorBarbeiro, ControladorServico, ControladorRecesso, ControladorAgendaMensal
from models import Endereco, Barbeiro, HorarioFuncionamento, AgendaMensal, Recesso, FaltaJustificadaBarbeiro, Cliente
from enums import EnumStatusMensagens, EnumNomesPastaImagem
from datetime import datetime, timezone, date


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
    email_digitado = request.form.get('gestor-email-2','')
    senha_digitada = request.form.get('gestor-password','')
    
    return ControladorGestor.login_gestor(email_digitado, senha_digitada)


# Logout Gestor - Encerramento da sessão do Gestor
@gestor.route('/logout', methods=['POST','GET'])
def gestorLogout():
    session.clear()
    return redirect(url_for('gestor.gestorLogin'))


# Painel Gestor - Aba inicial
@gestor.route('/painel', methods=['POST','GET'])
def gestorPainel():
    return ControladorGestor.consultar_agendamentos_data_hoje(date.today())

# Painel Gestor - Aba de visualização da Agenda de todos os Barbeiros
@gestor.route('/painel/agendamento')
def gestorAbaAgendamento():
    return render_template('pages/gestor/gestor-painel-agendamento-rp.html')

##################################################################################
#  HORARIO_FUNCIONAMENTO

@gestor.route('/painel/horario_funcionamento')
def gestor_horario_funcionamento_barbearia():
    data_atual = datetime.now(timezone.utc).date()
    return render_template('pages/gestor/gestor-painel-agenda-rp.html', data_atual=data_atual,modo=0, botao_filtro=0,  horario_funcionamento = ControladorGestor.consultar_horario_funcionamento(1), agendas = ControladorAgendaMensal.consultar_todas_agendas_mensais_service() ,mensagens_status=EnumStatusMensagens)

@gestor.route('/painel/horario_funcionamento/consultar/mes_atual')
def gestor_horario_funcionamento_barbearia_consultar_mes():
    data_atual = datetime.now(timezone.utc).date()
    return render_template('pages/gestor/gestor-painel-agenda-rp.html', data_atual=data_atual,modo=1, botao_filtro=1,  horario_funcionamento = ControladorGestor.consultar_horario_funcionamento(1), agendas = ControladorAgendaMensal.consultar_agendas_mensais_por_mes_service() ,mensagens_status=EnumStatusMensagens)

@gestor.route('/painel/horario_funcionamento/consultar/ano_atual')
def gestor_horario_funcionamento_barbearia_consultar_ano():
    data_atual = datetime.now(timezone.utc).date()
    return render_template('pages/gestor/gestor-painel-agenda-rp.html', data_atual=data_atual,modo=1, botao_filtro=2,  horario_funcionamento = ControladorGestor.consultar_horario_funcionamento(1), agendas = ControladorAgendaMensal.consultar_agendas_mensais_anual_service() ,mensagens_status=EnumStatusMensagens)



@gestor.route('/painel/horario_funcionamento/atualizar', methods=['POST'])
def gestor_horario_funcionamento_barbearia_atualizar():
    
    horario_funcionamento = HorarioFuncionamento(
        id_horario=request.form.get("horario_funcionamento_id"),
        horario_abertura= datetime.strptime(request.form.get("horario_abertura", ''), "%H:%M").time(),
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
        data_inicio_recesso= datetime.strptime(request.form.get("data_inicio_recesso",''),  "%Y-%m-%d").date(),
        data_fim_recesso=datetime.strptime(request.form.get("data_fim_recesso",''),  "%Y-%m-%d").date(),
        descricao_recesso=request.form.get("descricao_recesso")
    )
     
    return ControladorRecesso.cadastrarRecesso(recesso)

@gestor.route('/painel/recessos', methods=['GET'])
def gestor_recesso_consultar():   
    return render_template('pages/gestor/gestor-painel-recesso-rp.html', modo=0, botao_filtro=0, recessos = ControladorRecesso.consultarRecessos(), mensagens_status=EnumStatusMensagens)

@gestor.route('/painel/recessos/consultar/mes_atual', methods=['GET'])
def gestor_recesso_consultar_mes_atual():   
    return render_template('pages/gestor/gestor-painel-recesso-rp.html', modo=1, botao_filtro=1, recessos = ControladorRecesso.consultarRecessosMesAtual(), mensagens_status=EnumStatusMensagens)

@gestor.route('/painel/recessos/consultar/ano_atual', methods=['GET'])
def gestor_recesso_consultar_ano_atual():   
    return render_template('pages/gestor/gestor-painel-recesso-rp.html', modo=1, botao_filtro=2, recessos = ControladorRecesso.consultarRecessosAnoAtual(), mensagens_status=EnumStatusMensagens)

@gestor.route('/painel/recessos/excluir', methods=['POST'])
def gestor_recesso_excluir():  
    recesso = Recesso(
        id_recesso=request.form.get("recesso-id", type=int),
        descricao_recesso=request.form.get("recesso-descricao")
    ) 
    return ControladorRecesso.excluirRecessos(recesso)

@gestor.route('/painel/recessos/atualizar', methods=['POST'])
def gestor_recesso_atualizar():  
       
    recesso = Recesso(
        id_recesso=request.form.get("id_recesso", type=int),
        data_inicio_recesso= datetime.strptime(request.form.get("data_inicio_recesso",''),  "%Y-%m-%d").date(),
        data_fim_recesso=datetime.strptime(request.form.get("data_fim_recesso",''),  "%Y-%m-%d").date(),
        descricao_recesso=request.form.get("descricao_recesso")
    ) 
    return ControladorRecesso.atualizarRecesso(recesso)

##################################################################################
# AGENDA MENSAL
@gestor.route('/painel/agenda_mensal/cadastrar', methods=['POST'])
def gestorAgendaCadastrar():
    
    agenda_mensal = AgendaMensal(
        data_inicial_mes= datetime.strptime(request.form.get("data_inicio",''),  "%Y-%m-%d").date(),
        data_final_mes=datetime.strptime(request.form.get("data_fim",''),  "%Y-%m-%d").date(),
        titulo_agenda=request.form.get("titulo_agenda"), 
        status_agenda_mensal=False
    )
     
    return ControladorAgendaMensal.cadastrar_agenda_mensal_service(agenda_mensal)

@gestor.route('/painel/agenda_mensal/atualizar', methods=['POST'])
def gestor_agenda_mensal_atualizar():
    
    
    agenda_mensal = AgendaMensal(
        id_agenda_mensal=request.form.get("agenda_id", type=int),
        data_inicial_mes= datetime.strptime(request.form.get("data_inicio",''),  "%Y-%m-%d").date(),
        data_final_mes=datetime.strptime(request.form.get("data_fim",''),  "%Y-%m-%d").date(),
        titulo_agenda=request.form.get("titulo_agenda")
    )
     
    return ControladorAgendaMensal.atualizar_agenda_mensal_service(agenda_mensal)

@gestor.route('/painel/agenda_mensal/alterar_status', methods=['POST'])
def gestor_agenda_mensal_alterar_status():
        
    status_agenda_mensal = request.form.get("status_agenda_mensal", type=int)
       
    agenda_mensal = AgendaMensal(
            id_agenda_mensal=request.form.get("agenda_id", type=int),
            data_inicial_mes= datetime.strptime(request.form.get("data_inicio",''),  "%Y-%m-%d").date(),
            data_final_mes=datetime.strptime(request.form.get("data_fim",''),  "%Y-%m-%d").date(),
            titulo_agenda=request.form.get("titulo_agenda"),
            status_agenda_mensal= not status_agenda_mensal
    )
    
       
    return ControladorAgendaMensal.atualizar_status_agenda_mensal_service(agenda_mensal)


##################################################################################
# SERVIÇOS - Aba de visualização de todos Serviços cadastrados
@gestor.route('/painel/servicos')
def gestorAbaServicos():     
    return ControladorServico.consultar_servicos()

@gestor.route('/painel/servicos/consulta/nome', methods=["POST"])
def gestor_consultar_servico_nome(): 
    nome_servico = request.form.get("consultar-servico")    
    return ControladorServico.consultarServicoNome(nome_servico)


#=================================================================================================
# SERVIÇOS - pagina para cadastrar o Serviço
@gestor.route('/painel/servicos/cadastrar', methods=['GET'])
def gestorServicoPageCadastrar():
    return render_template('pages/gestor/gestor-gerenciar-servico-rp.html', mensagens_status=EnumStatusMensagens)

# SERVIÇOS - Rota para enviar o serviço par ao cadastro
@gestor.route('/painel/servicos/cadastrar', methods=['POST'])
def gestorServicoCadastrar():
    
    imagem = request.files.get('srv-imagem', None)
    
    descricao_servico = request.form.get('srv-descricao-servico','').strip()
    valor = request.form.get('srv-valor','').strip()
    duracao = request.form.get('srv-duracao','').strip()

    return ControladorServico.cadastrarServico(imagem, descricao_servico, valor, duracao)

# SERVIÇOS - REMOVER
@gestor.route('/painel/servicos/excluir', methods=['POST'])
def gestor_excluir_servico(): 
    id_servico = request.form.get('srv-id-deletar')
    foto_nome = request.form.get('srv-foto_nome') 
    nome_servico = request.form.get('srv-nome') 
        
    return ControladorServico.excluirServico(id_servico, foto_nome, nome_servico)
  

# SERVIÇOS - Salvar edição do serviço no banco de dados
@gestor.route('/painel/servicos/editar', methods=['POST'])
def gestorServicoEditar():

    imagem_form = request.files.get('srv-imagem')
    img_padrao = request.form.get('imagem-padrao', None)
    imagem_anterior = request.form.get('srv-foto_nome_anterior')
  
    descricao_servico = request.form.get('srv-descricao-servico','')
    valor = request.form.get('srv-valor','').strip()
    duracao = request.form.get('srv-duracao','').strip()
    ativo = request.form.get('srv-status', type=int)
    id = request.form.get('srv-id')
  
    return ControladorServico.editarServico(id, imagem_form, img_padrao, imagem_anterior, descricao_servico, valor, duracao, ativo)

##################################################################################
# FALTAS JUSTIFICADAS DOS BARBEIROS - Aba de visualização dos Barbeiros cadastrados

@gestor.route('/painel/barbeiros/faltas-justificadas', methods=['GET'])
def gestor_faltas_justificadas_barbeiro():
    return render_template('pages/gestor/gestor-painel-barbeiros-faltas-justificadas-rp .html',modo=0, barbeiros_faltas_justificadas = ControladorBarbeiro.consultar_faltas_do_barbeiro_ativos(), botao_mes=0,  mensagens_status=EnumStatusMensagens)

@gestor.route('/painel/barbeiros/faltas-justificadas/consultar/mensal', methods=['GET'])
def gestor_faltas_justificadas_consultar_mensal_barbeiro():
    return render_template('pages/gestor/gestor-painel-barbeiros-faltas-justificadas-rp .html', modo=  1, barbeiros_faltas_justificadas = ControladorBarbeiro.consultar_faltas_mensais_barbeiros_ativos(), botao_mes=1, mensagens_status=EnumStatusMensagens)

@gestor.route('/painel/barbeiros/faltas-justificadas/consultar/anual', methods=['GET'])
def gestor_faltas_justificadas_consultar_anual_barbeiro():
    return render_template('pages/gestor/gestor-painel-barbeiros-faltas-justificadas-rp .html', modo=  1, barbeiros_faltas_justificadas = ControladorBarbeiro.consultar_faltas_anual_barbeiros_ativos(), botao_mes=2, mensagens_status=EnumStatusMensagens)

@gestor.route('/painel/barbeiros/faltas-justificadas/cadastrar', methods=['POST'])
def gestor_cadastrar_faltas_justificadas_barbeiro():

    id_barbeiro = request.form.get("id_barbeiro_falta", type=int)
    nome_barbeiro = request.form.get("nome_barbeiro_falta")
   
    falta_justificada = FaltaJustificadaBarbeiro(
        data_falta=datetime.strptime(request.form.get("data_falta",''),  "%Y-%m-%d").date(),
        horario_inicio_falta=request.form.get("hora_inicio_falta",''),
        horario_final_falta=request.form.get("hora_fim_falta",''),
        motivo_falta=request.form.get("motivo_falta_justificada",''),
        id_barbeiro=id_barbeiro
    )
    
    return ControladorBarbeiro.cadastrar_faltas_do_barbeiro_ativos(falta_justificada, nome_barbeiro)

@gestor.route('/painel/barbeiros/faltas-justificadas/excluir', methods=['POST'])
def gestor_excluir_faltas_justificadas_barbeiro():
    id_barbeiro = request.form.get("falta-id-barbeiro-excluir")
      
    falta_justificada = FaltaJustificadaBarbeiro(
        id_falta_justificada=request.form.get("falta-id-excluir", type=int),
        data_falta=datetime.strptime(request.form.get("falta-data-excluir",''),  "%Y-%m-%d").date(),
        horario_inicio_falta=request.form.get("falta-hora-inicial-excluir"),
        horario_final_falta=request.form.get("falta-hora-final-excluir"),
        motivo_falta= request.form.get("falta-motivo-excluir"),
        id_barbeiro=id_barbeiro
        )
    
    return ControladorBarbeiro.excluir_faltas_do_barbeiro_ativos(falta_justificada)

@gestor.route('/painel/barbeiros/faltas-justificadas/atualizar', methods=['POST'])
def gestor_atualizar_faltas_justificadas_barbeiro():
    id_barbeiro = request.form.get("id_barbeiro_falta")
    nome_barbeiro = request.form.get("nome_barbeiro_falta")
      
    falta_justificada = FaltaJustificadaBarbeiro(
        data_falta=datetime.strptime(request.form.get("data_falta",''),  "%Y-%m-%d").date(),
        horario_inicio_falta=request.form.get("hora_inicio_falta"),
        horario_final_falta=request.form.get("hora_fim_falta"),
        motivo_falta=request.form.get("motivo_falta_justificada"),
        id_falta_justificada=request.form.get("id_falta_justificativa", type=int)
        )
    return ControladorBarbeiro.atualizar_faltas_do_barbeiro_ativos(falta_justificada,nome_barbeiro)


##################################################################################
# BARBEIROS - Aba de visualização dos Barbeiros cadastrados

@gestor.route('/painel/barbeiros', methods=['GET'])
def gestorAbaBarbeiros():
    return render_template('pages/gestor/gestor-painel-barbeiros-rp.html',modo=0,  barbeiros = ControladorBarbeiro.consultar_todos_barbeiros(), mensagens_status=EnumStatusMensagens)

@gestor.route('/painel/barbeiro/consultar/nome', methods=['POST'])
def gestor_barbeiro_consultar_nome():
    nome_barbeiro = request.form.get("consultar-barbeiro")
    return render_template('pages/gestor/gestor-painel-barbeiros-rp.html', modo=1,  nome_barbeiro=nome_barbeiro, barbeiros = ControladorBarbeiro.consultar_barbeiros_nome(nome_barbeiro), mensagens_status=EnumStatusMensagens)

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
    agora_utc = datetime.now()
    
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
        foto_usuario=None,
        status_usuario=True,
        data_cadastro=datetime.now(),
        data_ultimo_acesso=datetime.now(),
        data_liberacao=datetime.now(),
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
    
    telefone_temp = ''.join(filter(str.isdigit,request.form.get('telefone')))
    
     
    barbeiro = Barbeiro(
        id_usuario=request.form.get('srv-id'),
        nome_completo=request.form.get('nome'),
        cpf=cpf_temp,
        telefone=telefone_temp,
        email=request.form.get('email'),
        senha=request.form.get('senha', None),
        data_ultimo_acesso=datetime.now(timezone.utc),
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

@gestor.route('/painel/cliente/consultar/nome',methods=['POST'])
def gestor_consultar_cliente():
    nome_cliente = request.form.get("consultar-cliente");
    return ControladorGestor.consultar_cliente_nome(nome_cliente)

@gestor.route('/painel/clientes/excluir', methods=['POST'])
def gestor_excluir_cliente():
    id_cliente = request.form.get("id_cliente_barbearia")
    foto_nome_cliente = request.form.get("foto_usuario")
    nome_cliente = request.form.get("nome_cliente_barbearia")
    
    return ControladorGestor.excluir_cliente_barbearia(id_cliente,foto_nome_cliente,nome_cliente)

@gestor.route('/painel/clientes/atualizar', methods=['POST'])
def gestor_atualizar_cliente():
    
    telefone_temp = ''.join(filter(str.isdigit,request.form.get('cliente_telefone')))
     
    cliente = Cliente(
        id_usuario=request.form.get("cliente_id"),
        foto_usuario=EnumNomesPastaImagem.IMAGEM_PADRAO.value,
        nome_completo=request.form.get("cliente_nome"),
        telefone=telefone_temp,
        email=request.form.get("cliente_email"),
        senha=request.form.get("cliente_senha"),
        motivo_bloqueio=request.form.get("motivo_falta_justificada") if request.form.get("motivo_falta_justificada").strip() else None,
        status_usuario=request.form.get("status_cliente"),
        cpf= request.form.get("cliente_cpf") if request.form.get("cliente_cpf").strip() else None
    )
            
    return ControladorGestor.atualizar_cliente_barbearia(cliente)

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