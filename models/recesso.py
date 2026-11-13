
from datetime import datetime, timezone

class Recesso:

    def __init__(
        self,
        id_recesso = None,
        descricao_recesso = None,
        data_inicio_recesso = None,
        data_fim_recesso = None 
    ):
        self.__id_recesso = id_recesso
        self.__data_inicio_recesso = data_inicio_recesso
        self.__data_fim_recesso = data_fim_recesso
        self.__descricao_recesso = descricao_recesso
        
       

    @property
    def id_recesso(self):
        return self.__id_recesso

    @id_recesso.setter
    def id_recesso(self, value):
        self.__id_recesso = value

    @property
    def data_inicio_recesso(self):
        return self.__data_inicio_recesso

    @data_inicio_recesso.setter
    def data_inicio_recesso(self, value):
        self.__data_inicio_recesso = value

    @property
    def data_fim_recesso(self):
        return self.__data_fim_recesso

    @data_fim_recesso.setter
    def data_fim_recesso(self, value):
        self.__data_fim_recesso = value
        
    @property
    def horario_fim_intrajornada(self):
        return self.__horario_fim_intrajornada

    @horario_fim_intrajornada.setter
    def horario_fim_intrajornada(self, value):
        self.__horario_fim_intrajornada = value
   
    @property
    def descricao_recesso(self):
        return self.__descricao_recesso

    @descricao_recesso.setter
    def hordescricao_recessoario_fim_intrajornada(self, value):
        self.__descricao_recesso = value