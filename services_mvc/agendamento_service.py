import calendar
from datetime import date, datetime

from flask import flash

from repositorio import AgendamentoRepositorio
from models import Agendamento

class AgendamentoService:
    
    def __init__(self):
        self.__agendamento_repositorio = AgendamentoRepositorio()
             
    def consultar_agendamento_agendados(self, id_cliente): 
        return self.__agendamento_repositorio.consultarAgendamentoStatusAgendados(id_cliente)
    
    def consultar_agendamento_data_atual(self, data_hoje): 
        return self.__agendamento_repositorio.consultarAgendamentoDataAtual(data_hoje)
    
    def consultar_total_agendamento_cancelado_data_hoje(self, data_hoje): 
        return self.__agendamento_repositorio.consultarTotalAgendamentoCanceladoPorDia(data_hoje)
    
    def consultar_valor_ticket_medio_mensal_agendamento(self): 
        return self.__agendamento_repositorio.consultarMediaMensalAgendamento(date.today().replace(day=1),date.today().replace(day=calendar.monthrange(date.today().year, date.today().month)[1]))
    
    def consultar_total_agendamento(self, data_inicio, data_final): 
        return self.__agendamento_repositorio.consultarTotalAgendamentosPorPeriodo(data_inicio, data_final)

    def cadastrar_agendamento(self, agendamento):
        return self.__agendamento_repositorio.salvar(agendamento)
        
    def atualizar_status_e_motivo_do_cancelamento_service(self, motivo_cancelamento, status_agendamento,agenda_mensal):
        return self.__agendamento_repositorio.atualizarStatusMotivoDoCancelamentoAgendaMensal(motivo_cancelamento, status_agendamento,agenda_mensal)
    
    def atualizar_status_cancelamento_faltas_justificadas_service(self, motivo_cancelamento, status_agendamento,falta_justificada):
        return self.__agendamento_repositorio.atualizarStatusMotivoDoCancelamentoFaltasJustificadas(motivo_cancelamento, status_agendamento,falta_justificada)

    def alterar_status_agendamento(self, id_agendamento:int, status_agendamento:int):
        try:
            data_hoje = datetime.today()
            data_hoje = data_hoje.strftime("%Y-%m-%d")
            
            return self.__agendamento_repositorio.atualizar_status_agendamento(id_agendamento, status_agendamento, data_hoje)
        except Exception as erros: 
            print(f"\n ERRO NO SERVICE: {repr(erros)}\n\n")
            flash(f"\n\n # ERRO AO #\n {erros}\n\n")
            return 
    
    def cancelar_agendamento(self, id_agendamento:int, motivo_cancelamento):
        try:
            data_hoje = datetime.today()
            data_hoje = data_hoje.strftime("%Y-%m-%d")
            
            return self.__agendamento_repositorio.cancelar_agendamento(id_agendamento, data_hoje, motivo_cancelamento)
        except Exception as erros: 
            print(f"\n ERRO NO SERVICE: {repr(erros)}\n\n")
            flash(f"\n\n # ERRO AO #\n {erros}\n\n")
            return
    
    def consultar_agendamentos_por_periodo(self, data_inicio, data_fim):
        return self.__agendamento_repositorio.consultarAgendamentosPorPeriodo(data_inicio, data_fim)
    
    def consultar_agendamentos_por_barbeiro(self, id_barbeiro):
        return self.__agendamento_repositorio.listarPorBarbeiro(id_barbeiro)

    def cliente_tem_conflito_horario(self, id_cliente, data_agendamento, hora_inicio, hora_fim):
        return self.__agendamento_repositorio.clienteTemConflitoHorario(id_cliente, data_agendamento, hora_inicio, hora_fim)
    
    def atualizarStatusAgendamentoUsuarios(self, idAgendamento, status_agendamento, motivo_cancelamento):
        try:         
            return self.__agendamento_repositorio.atualizarStatusAgendamentoUsuarios(idAgendamento, status_agendamento, motivo_cancelamento)
        except Exception as erros: 
            print(f"\n ERRO NO SERVICE: {repr(erros)}\n\n") # <-- Vai mostrar o erro exato no terminal
            flash(f"\n\n # ERRO AO #\n {erros}\n\n")
            return 