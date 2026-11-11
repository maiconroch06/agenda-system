from repositorio import AgendaRepositorio
from models import Agenda

class AgendaService:
    
    def __init__(self):
        self.__agenda_repositorio = AgendaRepositorio()
        self.__agenda = Agenda()