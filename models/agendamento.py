from datetime import date, time, datetime
from .barbeiros import Barbeiro
from .cliente import Cliente
from .servicos import Servico


class Agendamento:

    def __init__(
        self,  
        data_agendamento: date,
        hora_inicio: time,
        hora_fim: time,
        status_agendamento: bool,
        data_atualizacao: datetime,
        servico: Servico,
        barbeiro: Barbeiro,
        cliente: Cliente,
        id_agendamento = None,
    ):
        self.__id_agendamento = id_agendamento
        self.__data_agendamento = data_agendamento
        self.__hora_inicio = hora_inicio
        self.__hora_fim = hora_fim
        self.__status_agendamento = status_agendamento
        self.__data_atualizacao = data_atualizacao
        self.__servico = servico
        self.__barbeiro = barbeiro
        self.__cliente = cliente

    @property
    def id_agendamento(self):
        return self.__id_agendamento

    @id_agendamento.setter
    def id_agendamento(self, value):
        self.__id_agendamento = value

    @property
    def data_agendamento(self):
        return self.__data_agendamento

    @data_agendamento.setter
    def data_agendamento(self, value):
        self.__data_agendamento = value

    @property
    def hora_inicio(self):
        return self.__hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, value):
        self.__hora_inicio = value

    @property
    def hora_fim(self):
        return self.__hora_fim

    @hora_fim.setter
    def hora_fim(self, value):
        self.__hora_fim = value

    @property
    def status_agendamento(self):
        return self.__status_agendamento

    @status_agendamento.setter
    def status_agendamento(self, value):
        self.__status_agendamento = value

    @property
    def data_atualizacao(self):
        return self.__data_atualizacao

    @data_atualizacao.setter
    def data_atualizacao(self, value):
        self.__data_atualizacao = value

    @property
    def servico(self):
        return self.__servico

    @servico.setter
    def servico(self, value):
        self.__servico = value

    @property
    def barbeiro(self):
        return self.__barbeiro

    @barbeiro.setter
    def barbeiro(self, value):
        self.__barbeiro = value

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, value):
        self.__cliente = value
 
    def _str__(self):
        return (
            f"Agendamento(id={self.__id}, "
            f"data={self.__data_agendamento}, "
            f"inicio={self.__hora_inicio}, "
            f"fim={self.__hora_fim}, "
            
        )
