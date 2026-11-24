from flask import flash

from enums.enum_status_mensagens import EnumStatusMensagens
from services_mvc import AgendamentoService

class ControladorAgendamento:
    __agendamentos = AgendamentoService()
    
    @classmethod
    def consultar_agendamento(cls, status_agendamento):
        return cls.__agendamentos.consultar_agendamento_agendados(status_agendamento)
    
    @classmethod
    def consultar_agendamento_data_atual(cls, data_hoje):
        return cls.__agendamentos.consultar_agendamento_data_atual(data_hoje)
    
    @classmethod
    def consultar_agendamento_filtros(cls, barbeiro_id,  status,servico_id,data_inicio,data_fim):
        return cls.__agendamentos.consultar_agendamento_filtros(barbeiro_id, status,servico_id,data_inicio,data_fim)
    
    @classmethod
    def consultar_total_agendamento_cancelado_por_dia(cls, data_hoje):
        return cls.__agendamentos.consultar_total_agendamento_cancelado_data_hoje(data_hoje)
   
    @classmethod
    def consultar_valor_ticket_medio_mensal_agendamento(cls):
        return cls.__agendamentos.consultar_valor_ticket_medio_mensal_agendamento()
    
    @classmethod
    def atualizar_status_agendamento(cls, id_agendamento:int, status_agendamento:int, motivo_cancelamento):
        try:
            cls.__agendamentos.atualizarStatusAgendamentoUsuarios(id_agendamento, status_agendamento, motivo_cancelamento)
            flash("Agendamento alterado com sucesso", EnumStatusMensagens.SUCESSO.value)
        except Exception as erros:
            flash(f"Não foi possivel alterar o status do agendamento, contate o suporte", EnumStatusMensagens.AVISO.value)
            flash(f"{erros}")