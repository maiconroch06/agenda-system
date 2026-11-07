
from datetime import datetime, timezone

class Agenda:

    def __init__(
        self,
        id = None,
        descricao = None,
        data_criacao = datetime.now(timezone.utc),
        ativo = True
    ):
        self.__id = id
        self.__descricao = descricao
        self.__data_criacao = data_criacao
        self.__ativo = ativo

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, value):
        self.__descricao = value

    @property
    def data_criacao(self):
        return self.__data_criacao

    @data_criacao.setter
    def data_criacao(self, value):
        self.__data_criacao = value

    @property
    def ativo(self):
        return self.__ativo

    @ativo.setter
    def ativo(self, value):
        self.__ativo = value


    def __str__(self):
        return (
            f"Agenda(id={self.__id}, "
            f"descricao='{self.__descricao}', "
            f"data_criacao={self.__data_criacao}, "
            f"ativo={self.__ativo})"
        )
