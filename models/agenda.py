
from datetime import datetime, timezone

class Agenda:

    def __init__(
        self,
        id_agenda = None,
        horario_abertura = None,
        horario_fechamento = None,
        horario_inicio_intrajornada = None,
        horario_fim_intrajornada = None
    ):
        self.__id_agenda = id_agenda
        self.__horario_abertura = horario_abertura
        self.__horario_fechamento = horario_fechamento
        self.__horario_inicio_intrajornada = horario_inicio_intrajornada
        self.__horario_fim_intrajornada = horario_fim_intrajornada

    @property
    def id_agenda(self):
        return self.__id_agenda

    @id_agenda.setter
    def id_agenda(self, value):
        self.__id_agenda = value

    @property
    def horario_abertura(self):
        return self.__horario_abertura

    @horario_abertura.setter
    def horario_abertura(self, value):
        self.__horario_abertura = value

    @property
    def horario_fechamento(self):
        return self.__horario_fechamento

    @horario_fechamento.setter
    def horario_fechamento(self, value):
        self.__horario_fechamento = value

    @property
    def horario_inicio_intrajornada(self):
        return self.__horario_inicio_intrajornada

    @horario_inicio_intrajornada.setter
    def horario_inicio_intrajornada(self, value):
        self.__horario_inicio_intrajornada = value

    @property
    def horario_fim_intrajornada(self):
        return self.__horario_fim_intrajornada

    @horario_fim_intrajornada.setter
    def horario_fim_intrajornada(self, value):
        self.__horario_fim_intrajornada = value