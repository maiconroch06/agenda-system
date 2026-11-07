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
        self.__id = id
        self.__descricao = descricao
        self.__valor = valor
        self.__duracao = duracao
        self.__foto_nome = foto_nome
        self.__status_servico = status_servico
        self.__data_cadastro = data_cadastro
        self.__data_atualizacao = data_atualizacao

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, value):
        self.__descricao = value

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
    def foto_nome(self):
        return self.__foto_nome

    @foto_nome.setter
    def foto_nome(self, value):
        self.__foto_nome = value

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

    def _str__(self):
        return (
            f"Servico(id={self.__id}, "
            f"descricao='{self.__descricao}', "
            f"valor={self.__valor}, "
            f"duracao={self.__duracao} minutos, "
            f"status={self.__status_servico})"
        )
    
    # === vALIDAÇÕES ================    
    def valoresValidos(self):
        if self.__valor <= Decimal("0") or self.__duracao < -1 :
            raise Exception("Verifique se foi informado algum valor negativo!")
        
    def valoresVazios(self):
        if not self.__descricao.strip() or  self.__valor <= Decimal("0") or  self.__duracao < -1:
           raise Exception("Campos vazios! Verifique se os campos estão vazios!")
               