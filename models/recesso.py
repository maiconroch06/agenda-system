
from datetime import date
from .mes_referencia import MesReferencia


class Recesso:

    def __init__(
        self,
        data_dia: date,
        descricao_feriado: str,
        mes_referencia: MesReferencia,
        id: int = None
    ):
        self.__id = id
        self.__data_dia = data_dia
        self.__descricao_feriado = descricao_feriado
        self.__mes_referencia = mes_referencia

    @property
    def id(self):
        return self.__id

    @property
    def data_dia(self):
        return self.__data_dia

    @data_dia.setter
    def data_dia(self, value):
        self.__data_dia = value

    @property
    def descricao_feriado(self):
        return self.__descricao_feriado

    @descricao_feriado.setter
    def descricao_feriado(self, value):
        self.__descricao_feriado = value

    @property
    def mes_referencia(self):
        return self.__mes_referencia

    @mes_referencia.setter
    def mes_referencia(self, value):
        self.__mes_referencia = value

    def __str__(self):
        return (
            f"Recesso("
            f"id='{self.__id}', "
            f"data='{self.__data_dia}', "
            f"descricao='{self.__descricao_feriado}')"
        )
