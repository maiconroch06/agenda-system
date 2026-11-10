
from datetime import date, time
from .barbeiros import Barbeiro


class FaltaJustificadaBarbeiro:

    def __init__(
        self,
        data_falta: date,
        horario_inicio_falta: time,
        horario_final_falta: time,
        motivo_falta: str,
        barbeiro: Barbeiro,
        id: int = None
    ):
        self.__id = id
        self.__data_falta = data_falta
        self.__horario_inicio_falta = horario_inicio_falta
        self.__horario_final_falta = horario_final_falta
        self.__motivo_falta = motivo_falta
        self.__barbeiro = barbeiro

    @property
    def id(self):
        return self.__id

    @property
    def data_falta(self):
        return self.__data_falta

    @data_falta.setter
    def data_falta(self, value):
        self.__data_falta = value

    @property
    def horario_inicio_falta(self):
        return self.__horario_inicio_falta

    @horario_inicio_falta.setter
    def horario_inicio_falta(self, value):
        self.__horario_inicio_falta = value

    @property
    def horario_final_falta(self):
        return self.__horario_final_falta

    @horario_final_falta.setter
    def horario_final_falta(self, value):
        self.__horario_final_falta = value

    @property
    def motivo_falta(self):
        return self.__motivo_falta

    @motivo_falta.setter
    def motivo_falta(self, value):
        self.__motivo_falta = value

    @property
    def barbeiro(self):
        return self.__barbeiro

    @barbeiro.setter
    def barbeiro(self, value):
        self.__barbeiro = value
