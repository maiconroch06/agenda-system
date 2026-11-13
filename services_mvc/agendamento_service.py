from repositorio import AgendamentoRepositorio
from models import Agendamento

class AgendamentoService:
    
    def __init__(self):
        self.__agendamento_repositorio = AgendamentoRepositorio()
        
        
    def consultar_agendamento_agendados(self, id_cliente): 
        return self.__agendamento_repositorio.consultar_agendamento_status_agendados(id_cliente)

    def cadastrar_agendamento(self, agendamento):
        return self.__agendamento_repositorio.salvar(agendamento)
        
    