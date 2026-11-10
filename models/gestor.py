from datetime import datetime
from models.usuarios import Usuario
from .endereco import Endereco


class Gestor(Usuario):

    def __init__(
        self,
        cnpj_barbearia,
        nome_completo, 
        telefone, 
        cpf, 
        email, 
        status_usuario, 
        data_cadastro, 
        data_atualizacao, 
        foto_nome_usuario=None, 
        senha=None, 
        id_usuario=None, 
        endereco = None
        ):
        
        super().__init__(
            nome_completo=nome_completo, 
            telefone=telefone, 
            cpf=cpf, 
            email=email, 
            status_usuario=status_usuario, 
            data_cadastro=data_cadastro,
            data_atualizacao=data_atualizacao, 
            foto_nome_usuario=foto_nome_usuario, 
            senha =senha, 
            id_usuario=id_usuario,
            endereco=endereco
            )

        self.__cnpj_barbearia = cnpj_barbearia

    @property
    def cnpj_barbearia(self):
        return self.__cnpj_barbearia

    @cnpj_barbearia.setter
    def cnpj_barbearia(self, value):
        self.__cnpj_barbearia = value


   
