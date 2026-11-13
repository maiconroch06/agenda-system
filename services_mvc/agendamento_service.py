from repositorio import AgendamentoRepositorio
from models import Agendamento

class AgendamentoService:
    
    def __init__(self):
        self.__agendamento_repositorio = AgendamentoRepositorio()
        
        
    def consultar_agendamento_agendados(self, id_cliente): 
        return self.__agendamento_repositorio.consultar_agendamento_status_agendados(id_cliente)

    def cadastrar_agendamento(self, agendamento):
        return self.__agendamento_repositorio.salvar(agendamento)
        
    def atualizar_status_e_motivo_do_cancelamento_service(self, motivo_cancelamento, status_agendamento,agenda_mensal):
        return self.__agendamento_repositorio.atualizar_status_e_motivo_do_cancelamento(motivo_cancelamento, status_agendamento,agenda_mensal)