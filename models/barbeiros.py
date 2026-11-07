from datetime import datetime
from .usuarios import Usuario
from .endereco import Endereco
from .agenda import Agenda


class Barbeiro(Usuario):

    def __init__(
        self,
        nome_completo: str,
        telefone: str,
        cpf: str,
        email: str,
        senha: str,
        foto_nome: str,
        status_usuario: bool,
        data_cadastro: datetime,
        data_atualizacao: datetime,
        data_liberacao: datetime,
        descricao: str,
        status_barbeiro: bool,
        agenda: Agenda | None = None,
        id = None,
        endereco: Endereco = None,
        
        
    ):
        super().__init__(
            id=id,
            nome_completo=nome_completo,
            telefone=telefone,
            cpf=cpf,
            email=email,
            senha=senha,
            foto_nome=foto_nome,
            status_usuario=status_usuario,
            data_cadastro=data_cadastro,
            data_atualizacao=data_atualizacao,
            endereco=endereco
        )

        self.__data_liberacao = data_liberacao
        self.__descricao = descricao
        self.__status_barbeiro = status_barbeiro
        self.__agenda = agenda

    @property
    def data_liberacao(self):
        return self.__data_liberacao

    @data_liberacao.setter
    def data_liberacao(self, value):
        self.__data_liberacao = value

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, value):
        self.__descricao = value

    @property
    def status_barbeiro(self):
        return self.__status_barbeiro

    @status_barbeiro.setter
    def status_barbeiro(self, value):
        self.__status_barbeiro = value

    @property
    def agenda(self):
        return self.__agenda

    @agenda.setter
    def agenda(self, value):
        self.__agenda = value


    
