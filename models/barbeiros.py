from datetime import datetime, timezone
from .usuarios import Usuario


class Barbeiro(Usuario):

    def __init__(
        self,
        nome_completo, 
        telefone, 
        cpf, 
        email, 
        status_usuario, 
        data_cadastro, 
        data_atualizacao,
        data_liberacao = datetime.now(timezone.utc), 
        data_inicio_carreira = None,
        status_barbeiro = True,
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

        self.__data_liberacao = data_liberacao
        self.__data_inicio_carreira = data_inicio_carreira
        self.__status_barbeiro = status_barbeiro
        

    @property
    def data_liberacao(self):
        return self.__data_liberacao

    @data_liberacao.setter
    def data_liberacao(self, value):
        self.__data_liberacao = value

    @property
    def data_inicio_carreira(self):
        return self.__data_inicio_carreira

    @data_inicio_carreira.setter
    def data_inicio_carreira(self, value):
        self.__data_inicio_carreira = value

    @property
    def status_barbeiro(self):
        return self.__status_barbeiro

    @status_barbeiro.setter
    def status_barbeiro(self, value):
        self.__status_barbeiro = value



    
