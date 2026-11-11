
from datetime import datetime, timezone

class Recesso:

    def __init__(
        self,
        id_recesso = None,
        data_recesso = None,
        descricao_recesso = None, 
       
    ):
        self.__id_recesso = id_recesso
        self.__data_recesso = data_recesso
        self.__descricao_recesso = descricao_recesso
        
       

    @property
    def id_recesso(self):
        return self.__id_recesso

    @id_recesso.setter
    def id_recesso(self, value):
        self.__id_recesso = value

    @property
    def data_recesso(self):
        return self.__data_recesso

    @data_recesso.setter
    def data_recesso(self, value):
        self.__data_recesso = value

    @property
    def descricao_recesso(self):
        return self.__descricao_recesso

    @descricao_recesso.setter
    def descricao_recesso(self, value):
        self.__descricao_recesso = value
        
    @property
    def horario_fim_intrajornada(self):
        return self.__horario_fim_intrajornada

    @horario_fim_intrajornada.setter
    def horario_fim_intrajornada(self, value):
        self.__horario_fim_intrajornada = value