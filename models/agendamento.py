from datetime import date, time, datetime


class Agendamento:

    def __init__(
        self,
        id: int,
        data_agendamento: date,
        hora_inicio: time,
        hora_fim: time,
        status_agendamento: bool,
        data_atualizacao: datetime,
        fk_id_servico: int,
        fk_id_barbeiro: int,
        fk_id_cliente: int
    ):
        self.id = id
        self.data_agendamento = data_agendamento
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.status_agendamento = status_agendamento
        self.data_atualizacao = data_atualizacao
        self.fk_id_servico = fk_id_servico
        self.fk_id_barbeiro = fk_id_barbeiro
        self.fk_id_cliente = fk_id_cliente

    def consultarDataAgendamento(self):
        return self.data_agendamento

    def atualizarDataAgendamento(self, data: date):
        self.data_agendamento = data

    def consultarHoraInicio(self):
        return self.hora_inicio

    def atualizarHoraInicio(self, hora: time):
        self.hora_inicio = hora

    def consultarHoraFim(self):
        return self.hora_fim

    def atualizarHoraFim(self, hora: time):
        self.hora_fim = hora

    def consultarStatusAgendamento(self):
        return self.status_agendamento

    def atualizarStatusAgendamento(self, status: bool):
        self.status_agendamento = status

    def consultarDataAtualizacao(self):
        return self.data_atualizacao

    def atualizarDataAtualizacao(self, data: datetime):
        self.data_atualizacao = data

    def consultarIdServico(self):
        return self.fk_id_servico

    def consultarIdBarbeiro(self):
        return self.fk_id_barbeiro

    def consultarIdCliente(self):
        return self.fk_id_cliente

    def validarHorario(self):
        return self.hora_inicio < self.hora_fim

    def __str__(self):
        return (
            f"Agendamento(id={self.id}, "
            f"data={self.data_agendamento}, "
            f"inicio={self.hora_inicio}, "
            f"fim={self.hora_fim}, "
            f"cliente={self.fk_id_cliente}, "
            f"barbeiro={self.fk_id_barbeiro})"
        )
