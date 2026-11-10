from datetime import datetime
from decimal import Decimal

class Servico:

    def __init__(
        self,
        id_servico: int | None = None,
        descricao_servico: str | None = None,
        valor: Decimal | None = None,
        duracao: int | None = None,
        foto_nome_servico: str | None = None,
        status_servico: bool | None = None,
        data_cadastro: datetime | None = None,
        data_atualizacao: datetime | None = None
    ):
        self.__id_servico = id_servico
        self.__descricao_servico = descricao_servico
        self.__valor = valor
        self.__duracao = duracao
        self.__foto_nome_servico = foto_nome_servico
        self.__status_servico = status_servico
        self.__data_cadastro = data_cadastro
        self.__data_atualizacao = data_atualizacao

    @property
    def id_servico(self):
        return self.__id_servico

    @id_servico.setter
    def id_servico(self, value):
        self.__id_servico = value

    @property
    def descricao_servico(self):
        return self.__descricao_servico

    @descricao_servico.setter
    def descricao_servico(self, value):
        self.__descricao_servico = value

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, value):
        self.__valor = value

    @property
    def duracao(self):
        return self.__duracao

    @duracao.setter
    def duracao(self, value):
        self.__duracao = value

    @property
    def foto_nome_servico(self):
        return self.__foto_nome_servico

    @foto_nome_servico.setter
    def foto_nome_servico(self, value):
        self.__foto_nome_servico = value

    @property
    def status_servico(self):
        return self.__status_servico

    @status_servico.setter
    def status_servico(self, value):
        self.__status_servico = value

    @property
    def data_cadastro(self):
        return self.__data_cadastro

    @data_cadastro.setter
    def data_cadastro(self, value):
        self.__data_cadastro = value

    @property
    def data_atualizacao(self):
        return self.__data_atualizacao

    @data_atualizacao.setter
    def data_atualizacao(self, value):
        self.__data_atualizacao = value
    
    # === vALIDAÇÕES ================    
    def valoresValidos(self):
        if self.__valor <= Decimal("0") or self.__duracao < -1 :
            raise Exception("Verifique se foi informado algum valor negativo!")
        
    def valoresVazios(self):
        if not self.__descricao_servico.strip() or  self.__valor <= Decimal("0") or  self.__duracao < -1:
           raise Exception("Campos vazios! Verifique se os campos estão vazios!")
               