from datetime import date, time


class HorariosAgenda:

    def __init__(
        self,
        id: int,
        inicio_expediente: time,
        fim_expediente: time,
        data_mes: date,
        intervalo_descanco_inicio: time,
        intervalo_descanso_fim: time,
        dias_semana: str,
        fk_id_agenda: int
    ):
        self.id = id
        self.inicio_expediente = inicio_expediente
        self.fim_expediente = fim_expediente
        self.data_mes = data_mes
        self.intervalo_descanco_inicio = intervalo_descanco_inicio
        self.intervalo_descanso_fim = intervalo_descanso_fim
        self.dias_semana = dias_semana
        self.fk_id_agenda = fk_id_agenda

    def consultarInicioExpediente(self):
        return self.inicio_expediente

    def atualizarInicioExpediente(self, horario: time):
        self.inicio_expediente = horario

    def consultarFimExpediente(self):
        return self.fim_expediente

    def atualizarFimExpediente(self, horario: time):
        self.fim_expediente = horario

    def consultarDataMes(self):
        return self.data_mes

    def atualizarDataMes(self, data: date):
        self.data_mes = data

    def consultarIntervaloDescansoInicio(self):
        return self.intervalo_descanco_inicio

    def atualizarIntervaloDescansoInicio(self, horario: time):
        self.intervalo_descanco_inicio = horario

    def consultarIntervaloDescansoFim(self):
        return self.intervalo_descanso_fim

    def atualizarIntervaloDescansoFim(self, horario: time):
        self.intervalo_descanso_fim = horario

    def consultarDiaSemana(self):
        return self.dias_semana

    def atualizarDiaSemana(self, dia: str):
        self.dias_semana = dia

    def consultarIdAgenda(self):
        return self.fk_id_agenda

    def atualizarIdAgenda(self, id_agenda: int):
        self.fk_id_agenda = id_agenda

    def validarHorarioExpediente(self):
        return self.inicio_expediente < self.fim_expediente

    def validarIntervaloDescanso(self):
        return (
            self.inicio_expediente
            <= self.intervalo_descanco_inicio
            < self.intervalo_descanso_fim
            <= self.fim_expediente
        )

    def __str__(self):
        return (
            f"HorariosAgenda(id={self.id}, "
            f"inicio={self.inicio_expediente}, "
            f"fim={self.fim_expediente}, "
            f"dia='{self.dias_semana}', "
            f"id_agenda={self.fk_id_agenda})"
        )
