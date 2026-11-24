from flask import Blueprint, render_template, redirect, url_for, session, request
from controladores import ControladorBarbeiro
from enums import EnumStatusMensagens
from datetime import date, datetime, timedelta

barbeiro = Blueprint('barbeiro', __name__, template_folder='templates')

@barbeiro.route('/')
def barberSource():
    return redirect('/')

##################################################################################
# Logout Barbeiro - Encerramento da sessão do Barbeiro

@barbeiro.route('/logout', methods=['POST','GET'])
def barbeiroLogout():
    session.clear()
    return redirect('/')

##################################################################################
# Acesso do Barbeiro - Criação da sessão

@barbeiro.route('/login', methods=["POST"])
def barbeiroLogin():
    email_digitado = request.form.get('barbeiro-email-2','')
    senha_digitada = request.form.get('barbeiro-password','')
    
    return ControladorBarbeiro.login_barbeiro(email_digitado,senha_digitada)

##################################################################################
# Verificação Sesssão

@barbeiro.route('/login')
def barbeiroLoginPagina():
    if session.get('dados_barbeiro') is None:
        return render_template('pages/barbeiro/barbeiro-login.html', mensagens_status=EnumStatusMensagens)
        
    return redirect(url_for('barbeiro.barbeiroPainel'))

##################################################################################
# Painel de Visualização de Agendamentos

@barbeiro.route('/painel')
def barbeiroPainel():
    barbeiro = session.get('dados_barbeiro')
    if not barbeiro:
        return redirect(url_for('barbeiro.barbeiroLoginPagina'))

    if request.args.get('reset_data') == 'true':
        session.pop('data_exibicao_painel', None)
        return redirect(url_for('barbeiro.barbeiroPainel'))

    hoje = datetime.now().date()
    
    data_param = session.get('data_exibicao_painel')
    
    if data_param:
        try:
            data_exibicao = datetime.strptime(data_param, '%d/%m/%Y').date()
        except ValueError:
            data_exibicao = hoje
    else:
        data_exibicao = hoje

    data_str = data_exibicao.strftime('%d/%m/%Y')

    # Consultar agendamentos brutos
    agendamentos_brutos = ControladorBarbeiro.consultar_agendamentos_barbeiro(barbeiro.get('id_barbeiro'))
    
    # Filtrar pela data de exibição
    agendamentos = [a for a in agendamentos_brutos if a.get('data') == data_str]
    
    def peso_status(status):
        if status == 2: return 1
        elif status == 1: return 2
        elif status == 3: return 3
        else: return 4 
        
    agendamentos = sorted(
        agendamentos, key=lambda a: (peso_status(a.get('status')), a.get('hora_inicio', '00:00'))
    )

    # Cálculos para o Card de Progresso
    total = len(agendamentos)
    concluidos = sum(1 for a in agendamentos if a.get('status') == 2)
    cancelados = sum(1 for a in agendamentos if a.get('status') == 0)
    pendentes = total - concluidos - cancelados
    total_validos = total - cancelados

    pct_concluidos = (concluidos / total * 100) if total > 0 else 0
    pct_cancelados = (cancelados / total * 100) if total > 0 else 0
    pct_pendentes = (pendentes / total * 100) if total > 0 else 0

    # Formatação do texto de navegação
    if data_exibicao == hoje:
        data_display = "Hoje"
    elif data_exibicao == hoje + timedelta(days=1):
        data_display = "Amanhã"
    elif data_exibicao == hoje - timedelta(days=1):
        data_display = "Ontem"
    else:
        dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        data_display = f"{dias_semana[data_exibicao.weekday()]}, {data_exibicao.strftime('%d/%m')}"

    print(f"{agendamentos}")

    return render_template('pages/barbeiro/barbeiro-painel-inicio-rp.html',
                           barbeiro = barbeiro,
                            agendamentos = agendamentos,
                            concluidos = concluidos,
                            total_validos = total_validos,
                            pct_concluidos = pct_concluidos,
                            pct_cancelados = pct_cancelados,
                            pct_pendentes = pct_pendentes,
                            data_display = data_display,
                            is_hoje = (data_exibicao == hoje))

@barbeiro.route('/painel/navegar/<acao>')
def navegar_painel(acao):
    data_atual_str = session.get('data_exibicao_painel', datetime.now().strftime('%d/%m/%Y'))
    data_atual = datetime.strptime(data_atual_str, '%d/%m/%Y').date()

    if acao == 'proximo':
        nova_data = data_atual + timedelta(days=1)
    elif acao == 'anterior':
        nova_data = data_atual - timedelta(days=1)
    else:
        nova_data = datetime.now().date() # Se a ação for 'hoje'

    session['data_exibicao_painel'] = nova_data.strftime('%d/%m/%Y')

    return redirect(url_for('barbeiro.barbeiroPainel'))

@barbeiro.route('/atualizar_status/<id_agendamento>', methods=['POST'])
def atualizar_status(id_agendamento):
    status_agendamento = request.form.get('status')
    
    if status_agendamento == 'motivo':
        novo_status = 0
        motivo_cancelamento = request.form.get('motivo')
        print(f'\n\n{id_agendamento} - {motivo_cancelamento}\n\n')
                
        ControladorBarbeiro.cancelar_agendamento(id_agendamento, motivo_cancelamento)

    else:
        try:
            novo_status = int(status_agendamento)
        except (ValueError, TypeError):
            novo_status = status_agendamento
            
        ControladorBarbeiro.atualizar_status_agendamento(id_agendamento, novo_status)
    
    # Recarrega o painel após a alteração de status
    return redirect(url_for('barbeiro.barbeiroPainel'))

@barbeiro.before_request
def authentication():
    
    if 'dados_gestor' in session:
            return redirect(url_for('gestor.gestorLoginPagina'))
    
    if 'dados_cliente' in session:
        return redirect(url_for('cliente.clientAgendamentoServicos'))
            
    #Criando as minhas rotas publicas
    routers_publics = ['barbeiro.barbeiroLoginPagina','barbeiro.barbeiroLogin']
    
    # se a rota for publica ele retorna aqui e envia para a rota desejada;
    if request.endpoint  in routers_publics:
        return 
    
    # Se a rota não estiver nas rotas publicas ele verifica a sessão
    # Caso o usuario tente acessar uma rota privada ele redireciona para uma rota publica
    if 'dados_barbeiro' not in session:
        return redirect(url_for('barbeiro.barbeiroLoginPagina'))
    
    
