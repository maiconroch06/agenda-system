
import calendar
from datetime import date

from flask import flash

from repositorio import FaltaJustificadaBarbeiroRepositorio
from .agendamento_service import AgendamentoService
from enums import EnumStatusAgendamento

class FaltasJustificadaBarbeiroService:

    def __init__(self):
        self.__falta_justificadas_barbeiro_repositorio = FaltaJustificadaBarbeiroRepositorio()
        self.__agendamento_service = AgendamentoService()
    
    def cadastrar_falta_justificada(self, falta_justificada):
        
        if self.__falta_justificadas_barbeiro_repositorio.verificar_falta_justificativa_existente_barbeiro(falta_justificada):
            return False
        
        if self.__falta_justificadas_barbeiro_repositorio.cadastrar_falta_justificada(falta_justificada):
            motivo_cancelamento = "Motivo do cancelamento: " + falta_justificada.motivo_falta
            
            if self.__agendamento_service.consultar_total_agendamento(falta_justificada.data_falta, falta_justificada.data_falta):
                return self.__agendamento_service.atualizar_status_cancelamento_faltas_justificadas_service(motivo_cancelamento, EnumStatusAgendamento.CANCELADO.value, falta_justificada)
            
            return True
    
    def atualizar(self, falta_justificada):
        if self.__falta_justificadas_barbeiro_repositorio.verificar_atualizacao_falta_justificativa_existente_barbeiro(falta_justificada):
            return False
        
        if self.__falta_justificadas_barbeiro_repositorio.atualizar(falta_justificada):
            if self.__agendamento_service.consultar_total_agendamento(falta_justificada.data_falta, falta_justificada.data_falta):
                motivo_cancelamento = "Motivo do cancelamento: " + falta_justificada.motivo_falta
                return self.__agendamento_service.atualizar_status_cancelamento_faltas_justificadas_service(motivo_cancelamento, EnumStatusAgendamento.CANCELADO.value, falta_justificada)
            return True
        
    def excluir(self, falta_justificada):  
        if self.__falta_justificadas_barbeiro_repositorio.excluir(falta_justificada.id_falta_justificada):
            if self.__agendamento_service.consultar_total_agendamento(falta_justificada.data_falta, falta_justificada.data_falta):
                return self.__agendamento_service.atualizar_status_cancelamento_faltas_justificadas_service(None, EnumStatusAgendamento.SERVICO_AGENDADO.value, falta_justificada) 
            return True
        
    def consultar_faltas_mensais_barbeiros_ativo(self):
        try:
            barbeiros = self.__falta_justificadas_barbeiro_repositorio.consultar_faltas_barbeiros_ativo_periodo(date.today().replace(day=1),date.today().replace(day=calendar.monthrange(date.today().year, date.today().month)[1]))
            return barbeiros
        except Exception:
            flash(f"Erro ao buscar os barbeiros cadastrados no banco, contate o suporte")
            
    def consultar_faltas_anuais_barbeiros_ativo(self):
        try:
            barbeiros = self.__falta_justificadas_barbeiro_repositorio.consultar_faltas_barbeiros_ativo_periodo(date.today().replace(day=1, month=1),date.today().replace(day=31, month=12))
            return barbeiros
        except Exception:
            flash(f"Erro ao buscar os barbeiros cadastrados no banco, contate o suporte")
    
    def consultar_faltas_justificadas_barbeiro(self):
        return self.__falta_justificadas_barbeiro_repositorio.consultar_faltas_por_barbeiro_ativo()
    
    def consultar_faltas_justificadas_barbeiro_periodo(self, data_inicio, data_final):
        return self.__falta_justificadas_barbeiro_repositorio.consultar_faltas_por_periodo(data_inicio,data_final)