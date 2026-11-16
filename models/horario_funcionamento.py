
class HorarioFuncionamento:

    def __init__(
        self,
        id_horario=None,
        horario_abertura=None,
        horario_fechamento=None,
        horario_inicio_intrajornada=None,
        horario_fim_intrajornada=None,
        dias_funcionamento=None
    ):
        self.__id_horario = id_horario
        self.__horario_abertura = horario_abertura
        self.__horario_fechamento = horario_fechamento
        self.__horario_inicio_intrajornada = horario_inicio_intrajornada
        self.__horario_fim_intrajornada = horario_fim_intrajornada
        self.__dias_funcionamento = dias_funcionamento if dias_funcionamento is not None else []

    @property
    def id_horario(self):
        return self.__id_horario

    @id_horario.setter
    def id_horario(self, value):
        self.__id_horario = value

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

    @property
    def dias_funcionamento(self):
        return self.__dias_funcionamento

    @dias_funcionamento.setter
    def dias_funcionamento(self, value):
        self.__dias_funcionamento = value if value is not None else []