from flask import Blueprint, render_template, redirect, url_for, session, request
from controladores import ControladorBarbeiro
from enums import EnumStatusMensagens
from datetime import datetime, timedelta

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
    email_digitado = request.form.get('barbeiro-email-2')
    senha_digitada = request.form.get('barbeiro-password')
    
    return ControladorBarbeiro.login_barbeiro(email_digitado,senha_digitada)

##################################################################################
# O que isso esta fazendo? A mesma função existe no gestor

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

    agendamentos_flask = ControladorBarbeiro.consultar_agendamentos_barbeiro(barbeiro)
    
    print("\n 1. BARBEIRO NA SESSÃO: ", barbeiro)
    print("\n 2. AGENDAMENTOS RETORNADOS: ", agendamentos_flask)
    
    # 1. Obter a data da URL ou usar hoje por padrão
    data_param = request.args.get('data')
    hoje = datetime.now().date()
    
    if data_param:
        try:
            data_exibicao = datetime.strptime(data_param, '%Y-%m-%d').date()
        except ValueError:
            data_exibicao = hoje
    else:
        data_exibicao = hoje

    data_str = data_exibicao.strftime('%Y-%m-%d')

    # Consultar agendamentos brutos
    agendamentos_brutos = ControladorBarbeiro.consultar_agendamentos_barbeiro(barbeiro)
    
    # Filtrar pela data de exibição
    agendamentos_flask = [a for a in agendamentos_brutos if a.get('data') == data_str]
    
    # Função auxiliar para definir a prioridade
    def peso_status(status):
        if status == 2:
            return 1
        elif status == 1:
            return 2
        elif status == 3:
            return 3
        else:
            return 4  # Cancelado
        
    agendamentos_flask = sorted(
        agendamentos_flask, key=lambda a: (peso_status(a.get('status')), a.get('hora', '00:00'))
    )

    # 4. Cálculos para o Card de Progresso
    total = len(agendamentos_flask)
    concluidos = sum(1 for a in agendamentos_flask if a.get('status') == 2)
    cancelados = sum(1 for a in agendamentos_flask if a.get('status') == 0)
    pendentes = total - concluidos - cancelados
    total_validos = total - cancelados

    pct_concluidos = (concluidos / total * 100) if total > 0 else 0
    pct_cancelados = (cancelados / total * 100) if total > 0 else 0
    pct_pendentes = (pendentes / total * 100) if total > 0 else 0

    # 5. Formatação do texto de navegação
    if data_exibicao == hoje:
        data_display = "Hoje"
    elif data_exibicao == hoje + timedelta(days=1):
        data_display = "Amanhã"
    elif data_exibicao == hoje - timedelta(days=1):
        data_display = "Ontem"
    else:
        dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        data_display = f"{dias_semana[data_exibicao.weekday()]}, {data_exibicao.strftime('%d/%m')}"

    # Variáveis para Jinja
    context = {
        'barbeiro': barbeiro,
        'agendamentos_flask': agendamentos_flask,
        'concluidos': concluidos,
        'total_validos': total_validos,
        'pct_concluidos': pct_concluidos,
        'pct_cancelados': pct_cancelados,
        'pct_pendentes': pct_pendentes,
        'data_display': data_display,
        'data_anterior': (data_exibicao - timedelta(days=1)).strftime('%Y-%m-%d'),
        'data_proxima': (data_exibicao + timedelta(days=1)).strftime('%Y-%m-%d'),
        'is_hoje': (data_exibicao == hoje)
    }

    return render_template('pages/barbeiro/barbeiro-painel-inicio-rp.html', **context)

@barbeiro.route('/atualizar_status/<id_agendamento>', methods=['POST'])
def atualizar_status(id_agendamento):
    status_agendamento = request.form.get('status')
    
    ControladorBarbeiro.atualizar_status_agendamento(id_agendamento, status_agendamento)
    
    # Recarrega o painel após a alteração de status
    return redirect(url_for('barbeiro.barbeiroPainel'))