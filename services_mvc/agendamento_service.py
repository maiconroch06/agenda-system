from repositorio import AgendamentoRepositorio
from models import Agendamento

class AgendamentoService:
    
    def __init__(self):
        self.__agendamento_repositorio = AgendamentoRepositorio()
        
        
    def consultar_agendamento(self): 
        return self.__agendamento_repositorio.listar_todos()

    def cadastrar_agendamento(self, agendamento):
        return self.__agendamento_repositorio.salvar(agendamento)
        
    