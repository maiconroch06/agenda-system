
from datetime import datetime


class Barbearia:

    def __init__(
        self,
        cnpj: str,
        nome_barbearia: str,
        telefone: str,
        email_empresa: str,
        logo_barbearia: str,
        data_cadastro: datetime,
        fk_id_endereco: int,
        fk_id_agenda: int
    ):
        self.cnpj = cnpj
        self.nome_barbearia = nome_barbearia
        self.telefone = telefone
        self.email_empresa = email_empresa
        self.logo_barbearia = logo_barbearia
        self.data_cadastro = data_cadastro
        self.fk_id_endereco = fk_id_endereco
        self.fk_id_agenda = fk_id_agenda

    def consultarCnpj(self):
        return self.cnpj

    def consultarNome(self):
        return self.nome_barbearia

    def atualizarNome(self, nome: str):
        self.nome_barbearia = nome

    def consultarTelefone(self):
        return self.telefone

    def atualizarTelefone(self, telefone: str):
        self.telefone = telefone

    def consultarEmail(self):
        return self.email_empresa

    def atualizarEmail(self, email: str):
        self.email_empresa = email

    def consultarLogo(self):
        return self.logo_barbearia

    def atualizarLogo(self, logo: str):
        self.logo_barbearia = logo

    def consultarDataCadastro(self):
        return self.data_cadastro

    def consultarIdEndereco(self):
        return self.fk_id_endereco

    def atualizarIdEndereco(self, id_endereco: int):
        self.fk_id_endereco = id_endereco

    def consultarIdAgenda(self):
        return self.fk_id_agenda

    def atualizarIdAgenda(self, id_agenda: int):
        self.fk_id_agenda = id_agenda

    def __str__(self):
        return (
            f"Barbearia(cnpj='{self.cnpj}', "
            f"nome='{self.nome_barbearia}', "
            f"telefone='{self.telefone}', "
            f"email='{self.email_empresa}')"
        )
