
from datetime import datetime, timezone

class MesReferencia:

    def __init__(
        self,
        id_mes_referencia = None,
        data_inicial_mes = None,
        data_final_mes = None,
        nome_mes = None,
        agenda = None
    ):
        self.__id_mes_referencia = id_mes_referencia
        self.__data_inicial_mes = data_inicial_mes
        self.__data_final_mes = data_final_mes
        self.__nome_mes = nome_mes
        self.__horario_fim_intrajornada = agenda

    @property
    def id_mes_referencia(self):
        return self.__id_mes_referencia

    @id_mes_referencia.setter
    def id_mes_referencia(self, value):
        self.__id_mes_referencia = value

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
    def horario_fim_intrajornada(self):
        return self.__horario_fim_intrajornada

    @horario_fim_intrajornada.setter
    def horario_fim_intrajornada(self, value):
        self.__horario_fim_intrajornada = value