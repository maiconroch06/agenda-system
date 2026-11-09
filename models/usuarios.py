from datetime import datetime
from typing import Optional
from models import Endereco

class Usuario:

    def __init__(
        self,
        nome_completo: str,
        telefone: str,
        cpf: str,
        email: str,
        status_usuario: bool,
        data_cadastro: datetime,
        data_atualizacao: datetime,
        foto_nome= None,
        senha=None,
        id = None,
        endereco: Endereco = None
    ):
        self.__id = id
        self.__nome_completo = nome_completo
        self.__telefone = telefone
        self.__cpf = cpf
        self.__email = email
        self.__senha = senha
        self.__foto_nome = foto_nome
        self.__status_usuario = status_usuario
        self.__data_cadastro = data_cadastro
        self.__data_atualizacao = data_atualizacao
        self.__endereco = endereco

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def nome_completo(self):
        return self.__nome_completo

    @nome_completo.setter
    def nome_completo(self, value):
        self.__nome_completo = value

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, value):
        self.__telefone = value

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, value):
        self.__cpf = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, value):
        self.__senha = value

    @property
    def foto_nome(self):
        return self.__foto_nome

    @foto_nome.setter
    def foto_nome(self, value):
        self.__foto_nome = value

    @property
    def status_usuario(self):
        return self.__status_usuario

    @status_usuario.setter
    def status_usuario(self, value):
        self.__status_usuario = value

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

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, value):
        self.__endereco = value


    # ========== VALIDAÇÕES DOS ATRIBUTOS =======
    def validarCPF(self):
        return bool(self.__cpf and self.__cpf.strip())

    def validarNome(self):
        return bool(self.__nome_completo and self.__nome_completo.strip())

    def validarEmail(self):
        return bool(self.__email and self.__email.strip())

    def validarTelefone(self):
        return bool(self.__telefone and self.__telefone.strip())

    def validarSenha(self):
        return bool(self.__senha and self.__senha.strip())

    def nomeVazioUsuario(self):
        if not self.__nome_completo or self.__nome_completo is None:
            raise ValueError("O nome do usuário é obrigatório.")

    def _str__(self):
        return f"Usuario(id={self.__id}, nome={self.__nome_completo})"
    
    def getTipo(self):
        return type(self).__name__