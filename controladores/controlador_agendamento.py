from services_mvc import AgendamentoService

class ControladorAgendamento:
    __agendamentos = AgendamentoService()
    
    @classmethod
    def consultar_agendamento(cls, status_agendamento):
        return cls.__agendamentos.consultar_agendamento(status_agendamento)