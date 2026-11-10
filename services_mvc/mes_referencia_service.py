from models import MesReferencia
from repositorio import MesReferenciaRepositorio

class MesReferenciaService:

    def __init__(self):
        self.__mes_referencia_repositorio = MesReferenciaRepositorio()
        self.__mes_referencia = MesReferencia()