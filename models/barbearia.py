
from datetime import datetime
from .endereco import Endereco
from .agenda import Agenda


class Barbearia:

    def __init__(
        self,
        cnpj: str,
        nome_barbearia: str,
        telefone: str,
        email_empresa: str,
        logo_barbearia: str,
        data_cadastro: datetime,
        endereco: Endereco,
        agenda: Agenda,
    ):
        self.__cnpj = cnpj
        self.__nome_barbearia = nome_barbearia
        self.__telefone = telefone
        self.__email_empresa = email_empresa
        self.__logo_barbearia = logo_barbearia
        self.__data_cadastro = data_cadastro
        self.__endereco = endereco
        self.__agenda = agenda

    @property
    def cnpj(self):
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, value):
        self.__cnpj = value

    @property
    def nome_barbearia(self):
        return self.__nome_barbearia

    @nome_barbearia.setter
    def nome_barbearia(self, value):
        self.__nome_barbearia = value

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, value):
        self.__telefone = value

    @property
    def email_empresa(self):
        return self.__email_empresa

    @email_empresa.setter
    def email_empresa(self, value):
        self.__email_empresa = value

    @property
    def logo_barbearia(self):
        return self.__logo_barbearia

    @logo_barbearia.setter
    def logo_barbearia(self, value):
        self.__logo_barbearia = value

    @property
    def data_cadastro(self):
        return self.__data_cadastro

    @data_cadastro.setter
    def data_cadastro(self, value):
        self.__data_cadastro = value

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, value):
        self.__endereco = value

    @property
    def agenda(self):
        return self.__agenda

    @agenda.setter
    def agenda(self, value):
        self.__agenda = value

    def __str__(self):
        return (
            f"Barbearia("
            f"cnpj='{self.__cnpj}', "
            f"nome='{self.__nome_barbearia}', "
            f"telefone='{self.__telefone}', "
            f"email='{self.__email_empresa}')"
        )
