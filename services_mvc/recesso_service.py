from models import Recesso
from repositorio import RecessoRepositorio

class RecessoService:

    def __init__(self):
        self.__recesso_repositorio = RecessoRepositorio()
        self.__recesso = Recesso()