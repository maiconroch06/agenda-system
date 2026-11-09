from datetime import datetime
from .servicos import Servico
from .barbeiros import Barbeiro

class BarbeiroHasServicos:

    def __init__(
        self,
        servico: Servico,
        barbeiro: Barbeiro,
        data_cadastro: datetime
    ):
        self.__servico = servico
        self.__barbeiro = barbeiro
        self.__data_cadastro = data_cadastro

    @property
    def barbeiro(self):
        return self.__barbeiro

    @barbeiro.setter
    def barbeiro(self, value):
        self.__barbeiro = value

    @property
    def data_cadastro(self):
        return self.__data_cadastro

    @data_cadastro.setter
    def data_cadastro(self, value):
        self.__data_cadastro = value

    def str__(self):
        return (
            f"BarbeiroHasServicos("
            f"id_servico={self.__id_servico}, "
            f"id_barbeiro={self.__id_barbeiro}, "
            f"data_cadastro={self.__data_cadastro})"
        )
