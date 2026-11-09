from datetime import datetime
from models import Usuario, Endereco

class Cliente(Usuario):

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
        endereco: Endereco = None,
        data_ultimo_servico: datetime = None,
        id = None,
    ):
        super().__init__(
            id = id,
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

        self.__data_ultimo_servico = data_ultimo_servico

    @property
    def data_ultimo_servico(self):
        return self.__data_ultimo_servico

    @data_ultimo_servico.setter
    def data_ultimo_servico(self, value):
        self.__data_ultimo_servico = value



    