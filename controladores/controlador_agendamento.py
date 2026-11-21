from services_mvc import AgendamentoService

class ControladorAgendamento:
    __agendamentos = AgendamentoService()
    
    @classmethod
    def consultar_agendamento(cls, status_agendamento):
        return cls.__agendamentos.consultar_agendamento_agendados(status_agendamento)
    
    @classmethod
    def consultar_agendamento_dia(cls, data_hoje):
        return cls.__agendamentos.consultar_agendamento_data_hoje(data_hoje)