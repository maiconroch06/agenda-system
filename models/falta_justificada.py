from datetime import datetime, timezone


class FaltaJustificada:

    def __init__(
        self,
        id_falta_justificada = None, 
        data_falta= None, 
        horario_inicio_falta= None, 
        horario_final_falta= None, 
        motivo_falta= None, 
        barbeiro = None, 
        ):

        self.__id_falta_justificada = id_falta_justificada
        self.__data_falta = data_falta
        self.__horario_inicio_falta = horario_inicio_falta
        self.__horario_final_falta = horario_final_falta
        self.__motivo_falta = motivo_falta
        self.__barbeiro = barbeiro
        

    @property
    def id_falta_justificada(self):
        return self.__id_falta_justificada

    @id_falta_justificada.setter
    def id_falta_justificada(self, value):
        self.__id_falta_justificada = value

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
    
