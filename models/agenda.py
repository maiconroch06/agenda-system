
from datetime import time


class Agenda:

    def __init__(
        self,
        horario_abertura: time,
        horario_fechamento: time,
        horario_inicio_intrajornada: time,
        horario_fim_intrajornada: time,
        id: int = None
    ):
        self.__id = id
        self.__horario_abertura = horario_abertura
        self.__horario_fechamento = horario_fechamento
        self.__horario_inicio_intrajornada = horario_inicio_intrajornada
        self.__horario_fim_intrajornada = horario_fim_intrajornada

    @property
    def id(self):
        return self.__id

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

    def __str__(self):
        return (
            f"Agenda("
            f"id='{self.__id}', "
            f"abertura='{self.__horario_abertura}', "
            f"fechamento='{self.__horario_fechamento}')"
        )