from repositorio import AgendamentoRepositorio
from models import Agendamento

class AgendamentoService:
    
    def __init__(self):
        self.agendamento_repositorio = AgendamentoRepositorio()
        
        
    def consultar_agendamento(self, status_agendamento): 
        return None
        
    