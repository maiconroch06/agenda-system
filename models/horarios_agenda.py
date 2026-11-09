from datetime import date, time
from .agenda import Agenda


class HorariosAgenda:

    def __init__(
        self,  
        inicio_expediente: time,
        fim_expediente: time,
        data_mes: date,
        intervalo_descanco_inicio: time | None = None,
        intervalo_descanso_fim: time  | None = None,
        dias_semana: str  | None = None,
        agenda: Agenda = None,
        id: int | None = None
    ):
        self.__id = id
        self.__inicio_expediente = inicio_expediente
        self.__fim_expediente = fim_expediente
        self.__data_mes = data_mes
        self.__intervalo_descanco_inicio = intervalo_descanco_inicio
        self.__intervalo_descanso_fim = intervalo_descanso_fim
        self.__dias_semana = dias_semana
        self.__agenda = agenda

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def inicio_expediente(self):
        return self.__inicio_expediente

    @inicio_expediente.setter
    def inicio_expediente(self, value):
        self.__inicio_expediente = value

    @property
    def fim_expediente(self):
        return self.__fim_expediente

    @fim_expediente.setter
    def fim_expediente(self, value):
        self.__fim_expediente = value

    @property
    def data_mes(self):
        return self.__data_mes

    @data_mes.setter
    def data_mes(self, value):
        self.__data_mes = value

    @property
    def intervalo_descanco_inicio(self):
        return self.__intervalo_descanco_inicio

    @intervalo_descanco_inicio.setter
    def intervalo_descanco_inicio(self, value):
        self.__intervalo_descanco_inicio = value

    @property
    def intervalo_descanso_fim(self):
        return self.__intervalo_descanso_fim

    @intervalo_descanso_fim.setter
    def intervalo_descanso_fim(self, value):
        self.__intervalo_descanso_fim = value

    @property
    def dias_semana(self):
        return self.__dias_semana

    @dias_semana.setter
    def dias_semana(self, value):
        self.__dias_semana = value

    @property
    def agenda(self):
        return self.__agenda

    @agenda.setter
    def agenda(self, value):
        self.__agenda = value

    def validarHorarioExpediente(self):
        return self.__inicio_expediente < self.__fim_expediente

    def validarIntervaloDescanso(self):
        return (
            self.__inicio_expediente
            <= self.__intervalo_descanco_inicio
            < self.__intervalo_descanso_fim
            <= self.__fim_expediente
        )

    def _str__(self):
        return (
            f"HorariosAgenda(id={self.__id}, "
            f"inicio={self.__inicio_expediente}, "
            f"fim={self.__fim_expediente}, "
            f"dia='{self.__dias_semana}', "
            f"id_agenda={self.__fk_id_agenda})"
        )
