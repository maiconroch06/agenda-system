from models import FaltaJustificadaBarbeiro
from repositorio import FaltaJustificadaBarbeiroRepositorio

class FaltasJustificadaBarbeiroService:

    def __init__(self):
        self.__falta_justificadas_barbeiro_repositorio = FaltaJustificadaBarbeiroRepositorio()
        self.__falta_justificadas_barbeiro = FaltaJustificadaBarbeiro()