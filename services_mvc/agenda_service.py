from repositorio import AgendaRepositorio
from models import Agenda

class AgendaService:
    
    def __init__(self):
        self.__agenda_repositorio = AgendaRepositorio()
        self.__agenda = Agenda()
        
    def cadastrar_agenda(self, descricao_agenda): 
        
        self.__agenda.descricao = "agenda de " + descricao_agenda
        self.__agenda.id = self.__agenda_repositorio.cadastrar_agenda(self.__agenda)
        
        return self.__agenda
        
    