from datetime import datetime
from models.usuarios import Usuario
from .endereco import Endereco


class Gestor(Usuario):

    def __init__(
        self,
        id: int,
        nome_completo: str,
        telefone: str,
        cpf: str,
        email: str,
        senha: str,
        foto_nome: str,
        status_usuario: bool,
        data_cadastro: datetime,
        data_atualizacao: datetime,
        fk_cnpj_barbearia: str,
        endereco: Endereco = None
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

        self.__fk_cnpj_barbearia = fk_cnpj_barbearia

    @property
    def fk_cnpj_barbearia(self):
        return self.__fk_cnpj_barbearia

    @fk_cnpj_barbearia.setter
    def fk_cnpj_barbearia(self, value):
        self.__fk_cnpj_barbearia = value


   
