from datetime import datetime
from decimal import Decimal

class Servico:

    def __init__(
        self,
        id: int | None = None,
        descricao: str | None = None,
        valor: Decimal | None = None,
        duracao: int | None = None,
        foto_nome: str | None = None,
        status_servico: bool | None = None,
        data_cadastro: datetime | None = None,
        data_atualizacao: datetime | None = None
    ):
        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.duracao = duracao
        self.foto_nome = foto_nome
        self.status_servico = status_servico
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    def consultarDescricao(self):
        return self.descricao

    def atualizarDescricao(self, descricao: str):
        self.descricao = descricao

    def consultarValor(self):
        return self.valor

    def atualizarValor(self, valor: Decimal):
        self.valor = valor

    def consultarDuracao(self):
        return self.duracao

    def atualizarDuracao(self, duracao: int):
        self.duracao = duracao

    def consultarFoto(self):
        return self.foto_nome

    def atualizarFoto(self, foto_nome: str):
        self.foto_nome = foto_nome

    def consultarStatus(self):
        return self.status_servico
    
    def ativarServico(self):
        self.status_servico = True

    def desativarServico(self):
        self.status_servico = False

    def consultarDataCadastro(self):
        return self.data_cadastro

    def consultarDataAtualizacao(self):
        return self.data_atualizacao

    def atualizarDataAtualizacao(self, data: datetime):
        self.data_atualizacao = data

    def __str__(self):
        return (
            f"Servico(id={self.id}, "
            f"descricao='{self.descricao}', "
            f"valor={self.valor}, "
            f"duracao={self.duracao} minutos, "
            f"status={self.status_servico})"
        )
        
    def valoresValidos(self):
        if self.valor <= Decimal("0") or self.duracao < -1 :
            raise Exception("Verifique se foi informado algum valor negativo!")
        
    def valoresVazios(self):
        if not self.descricao.strip() or  self.valor <= Decimal("0") or  self.duracao < -1:
           raise Exception("Campos vazios! Verifique se os campos estão vazios!")
               