
from datetime import datetime


class Agenda:

    def __init__(
        self,
        id: int,
        descricao: str,
        data_criacao: datetime,
        ativo: bool
    ):
        self.id = id
        self.descricao = descricao
        self.data_criacao = data_criacao
        self.ativo = ativo

    def consultarDescricao(self):
        return self.descricao

    def atualizarDescricao(self, descricao: str):
        self.descricao = descricao

    def consultarDataCriacao(self):
        return self.data_criacao

    def consultarStatus(self):
        return self.ativo

    def ativarAgenda(self):
        self.ativo = True

    def desativarAgenda(self):
        self.ativo = False

    def __str__(self):
        return (
            f"Agenda(id={self.id}, "
            f"descricao='{self.descricao}', "
            f"data_criacao={self.data_criacao}, "
            f"ativo={self.ativo})"
        )
