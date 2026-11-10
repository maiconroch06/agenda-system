
from datetime import date
from .agenda import Agenda


class MesReferencia:

    def __init__(
        self,
        data_inicial_mes: date,
        data_final_mes: date,
        nome_mes: str,
        agenda: Agenda,
        id: int = None
    ):
        self.__id = id
        self.__data_inicial_mes = data_inicial_mes
        self.__data_final_mes = data_final_mes
        self.__nome_mes = nome_mes
        self.__agenda = agenda

    @property
    def id(self):
        return self.__id

    @property
    def data_inicial_mes(self):
        return self.__data_inicial_mes

    @data_inicial_mes.setter
    def data_inicial_mes(self, value):
        self.__data_inicial_mes = value

    @property
    def data_final_mes(self):
        return self.__data_final_mes

    @data_final_mes.setter
    def data_final_mes(self, value):
        self.__data_final_mes = value

    @property
    def nome_mes(self):
        return self.__nome_mes

    @nome_mes.setter
    def nome_mes(self, value):
        self.__nome_mes = value

    @property
    def agenda(self):
        return self.__agenda

    @agenda.setter
    def agenda(self, value):
        self.__agenda = value

    def __str__(self):
        return (
            f"MesReferencia("
            f"id='{self.__id}', "
            f"nome='{self.__nome_mes}', "
            f"inicio='{self.__data_inicial_mes}', "
            f"fim='{self.__data_final_mes}')"
        )
