
from datetime import datetime, timezone

class AgendaMensal:

    def __init__(
        self,
        id_agenda_mensal = None,
        data_inicial_mes = None,
        data_final_mes = None,
        titulo_agenda = None,
        
    ):
        self.__id_agenda_mensal = id_agenda_mensal
        self.__data_inicial_mes = data_inicial_mes
        self.__data_final_mes = data_final_mes
        self.__titulo_agenda = titulo_agenda

    @property
    def id_agenda_mensal(self):
        return self.__id_agenda_mensal

    @id_agenda_mensal.setter
    def id_agenda_mensal(self, value):
        self.__id_agenda_mensal = value

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
    def titulo_agenda(self):
        return self.__titulo_agenda

    @titulo_agenda.setter
    def titulo_agenda(self, value):
        self.__titulo_agenda = value

    @property
    def horario_fim_intrajornada(self):
        return self.__horario_fim_intrajornada

    @horario_fim_intrajornada.setter
    def horario_fim_intrajornada(self, value):
        self.__horario_fim_intrajornada = value