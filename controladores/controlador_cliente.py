from models import Cliente
from flask import  session, redirect, url_for, flash, render_template
from models import Cliente, Agendamento
from database import db
from services_mvc import ClienteService, ServicoBarbearia, AgendaMensalService, BarbeariaService, BarbeiroService, AgendamentoService, AgendamentoServicosService, RecessoService, FaltasJustificadaBarbeiroService
from enums import EnumStatusMensagens
from flask import jsonify

class ControladorCliente():

    def __init__(self):
        self.__clienteService = ClienteService()
        self.__servicosServices = ServicoBarbearia()
        self.__agendaMensalService = AgendaMensalService()
        self.__barbeariaService = BarbeariaService()
        self.__barbeiroService = BarbeiroService()
        self.__agendamentoService = AgendamentoService()
        self.__agendamentoServicosService = AgendamentoServicosService()
        self.__recessoService = RecessoService()
        self.__faltasJustificadasBarbeiroService = FaltasJustificadaBarbeiroService()
    
    def login(self, email:str, senha:str):
        try:
            self.__clienteService.realizarLoginService(email,senha)
            return redirect(url_for('cliente.clientAgendamentoServicos'))
       
        except Exception as erros:
           flash(f"{erros}", EnumStatusMensagens.ERRO.value) 
           return  redirect(url_for('cliente.clientLoginPage'))
              
    def cadastrarCliente(self, cliente:Cliente):      
        try:
            cliente.id  =  self.__clienteService.cadastrarUsuarioService(cliente, cliente.foto_nome_usuario)
               
            if cliente.id:     
                if self.__clienteService.salvar_dados_especificos(cliente):                                      
                    return redirect(url_for('cliente.cadastroSucesso'))
            else:
                flash(f"Erro ao cadastrar o cliente", EnumStatusMensagens.ERRO.value)
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('cliente.clientRegisterPage'))

    # Lembrar de buscar os dias de recesso da agenda caso seja o ultimo dia
    # Buscar os dias Validos para agendamento
    # Validar Barbeiros Ativos
    # Validar Serviços Ativos
    # Horarios de Funciomento
    # Pegar Hora Atual para Agendamento
    # Buscar os Agendamentos já agendados
    # Buscar as faltas justificadas
    def gerenciarAgendamentoServico(self):
        try:
            dados_barbearia = self.__barbeariaService.buscar_todos_dados_barbearia()
            agenda_mensal = self.__agendaMensalService.consultar_ultima_agenda_cadastrada(dados_barbearia.cnpj)
            servicos = self.__servicosServices.listar_servicos_ativos()
            barbeiros = self.__barbeiroService.consultar_barbeiros_ativos()

            barbeiro_faltas_json = []
            agendamentos_json = []
            if agenda_mensal:

                barbeiro_faltas = self.__faltasJustificadasBarbeiroService.consultar_faltas_por_periodo(
                    agenda_mensal.data_inicial_mes,
                    agenda_mensal.data_final_mes
                )

                barbeiro_faltas_json = [
                    {
                        "id_barbeiro": falta["id_barbeiro"],
                        "data": falta["data_falta"].isoformat(),
                        "horario_inicio": falta["horario_inicio_falta"].strftime("%H:%M"),
                        "horario_fim": falta["horario_final_falta"].strftime("%H:%M"),
                        "motivo": falta["motivo_falta"]
                    }
                    for falta in barbeiro_faltas
                ]

                agendamentos_cadastrados = self.__agendamentoService.consultar_agendamentos_por_periodo(agenda_mensal.data_inicial_mes,
                                    agenda_mensal.data_final_mes)

                agendamentos_json = [
                    {
                        "id_barbeiro": agendamento.barbeiro.id_usuario,
                        "data": agendamento.data_agendamento.isoformat(),
                        "horario_inicio": agendamento.hora_inicio.strftime("%H:%M"),
                        "horario_fim": agendamento.hora_fim.strftime("%H:%M")
                    }
                    for agendamento in agendamentos_cadastrados
                ]

            recessos = self.__recessoService.consultar_recessos_services()

            recessos_json = [
                {
                    "data_inicio_recesso": recesso.data_inicio_recesso.isoformat(),
                    "data_fim_recesso": recesso.data_fim_recesso.isoformat(),
                    "descricao_recesso": recesso.descricao_recesso
                }
                for recesso in recessos
            ]

            horarios_barbearia = {
                "horario_abertura": dados_barbearia.agenda.horario_abertura.strftime("%H:%M"),
                "horario_fechamento": dados_barbearia.agenda.horario_fechamento.strftime("%H:%M"),
                "horario_inicio_intrajornada": dados_barbearia.agenda.horario_inicio_intrajornada.strftime("%H:%M"),
                "horario_fim_intrajornada": dados_barbearia.agenda.horario_fim_intrajornada.strftime("%H:%M")
            }

            return render_template('pages/cliente/cliente-agendamento-rp.html', 
                                   servicos=servicos, barbeiros=barbeiros, agenda_mensal=agenda_mensal, dados_barbearia=dados_barbearia, recessos=recessos_json, horarios_barbearia=horarios_barbearia, barbeiro_faltas=barbeiro_faltas_json, agendamentos=agendamentos_json, mensagens_status=EnumStatusMensagens)
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('cliente.clientLoginPage'))

    # Não posso cadastrar dois serviço com barbeiros diferentes no mesmo horário
    def cadastrarAgendamento(self, agendamento: Agendamento, id_servicos, id_barbeiro):
        try:
            conflito = self.__agendamentoService.cliente_tem_conflito_horario(agendamento.cliente.id_usuario, agendamento.data_agendamento, agendamento.hora_inicio, agendamento.hora_fim)
            if conflito:
                    flash("Conflito nos horários do agendamento",EnumStatusMensagens.AVISO.value)
                    return jsonify({
                        "redirect_url": url_for('cliente.clientAgendamentoServicos'),
                        "limpar_selecao": True
                    }), 409

            agendamento.barbeiro = self.__barbeiroService.buscar_barbeiro_id(id_barbeiro)
            id_agendamento = self.__agendamentoService.cadastrar_agendamento(agendamento)
            self.__agendamentoServicosService.salvar_agendamento_servicos(id_agendamento, id_servicos)

            flash("Agendamento cadastrado com sucesso!", EnumStatusMensagens.SUCESSO.value)
            return jsonify({
                "redirect_url": url_for('cliente.clientMeusAgendamentos'),
                "limpar_selecao": False
            }), 200
        
        except Exception as erros:
            print(f"ERRO AO CADASTRAR AGENDAMENTO: {erros}")
            return jsonify({
                "erro": "Não foi possível cadastrar o agendamento."
            }), 500

    # Motivo de Falta do barbeiro
    def meusAgendamentos(self, id_cliente):
        try:
            agendamentos = (
                self.__agendamentoServicosService
                .consultar_agendamentos_por_cliente(id_cliente)
            )

            print(agendamentos)

            total_proximos = sum(
                1 for item in agendamentos
                if item.agendamento.status_agendamento in (1, 2)
            )

            total_concluidos = sum(
                1 for item in agendamentos
                if item.agendamento.status_agendamento == 3
            )

            return render_template(
                'pages/cliente/cliente-meus-agendamentos.html',
                agendamentos=agendamentos,
                total_proximos=total_proximos,
                total_concluidos=total_concluidos,
                mensagens_status=EnumStatusMensagens
            )
            
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('cliente.clientLoginPage'))

   
    def consultar_todos_clientes(self):
        return self.__clienteService.consultar_clientes_services()
    
    def consultar_cliente_nome(self, nome_completo):
        return self.__clienteService.consultar_cliente_nome_services(nome_completo)
   
    def excluir_cliente(self, id_usuario, foto_nome, nome_pasta):
        return self.__clienteService.excluir_usuario_barbearia(id_usuario, foto_nome, nome_pasta)

    def atualziar_cliente(self, cliente):
        return self.__clienteService.alterar_usuario_barbearia(None, None,cliente.foto_nome_usuario,  cliente)


   