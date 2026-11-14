from models import Agendamento, Servico

class AgendamentoServicos:

    def __init__(
        self,
        agendamento: Agendamento = None,
        servicos: list[Servico] = None
    ):
        self.__agendamento = agendamento
        self.__servicos = servicos or []

    @property
    def agendamento(self):
        return self.__agendamento

    @agendamento.setter
    def agendamento(self, value):
        self.__agendamento = value

    @property
    def servicos(self):
        return self.__servicos

    @servicos.setter
    def servicos(self, value):
        self.__servicos = value