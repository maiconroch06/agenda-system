from repositorio import AgendaRepositorio
from models import Agenda

class AgendaService:
    
    def __init__(self):
        self.agenda_repositorio = AgendaRepositorio()
        self.agenda = Agenda()
        
    def cadastrar_agenda(self, descricao_agenda): 
        
        self.agenda.descricao = "agenda de " + descricao_agenda
        self.agenda.id = self.agenda_repositorio.cadastrar_agenda(self.agenda)
        
        return self.agenda
        
    