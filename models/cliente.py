from datetime import datetime
from models import Usuario, Endereco

class Cliente(Usuario):

    def __init__(
        self,
        nome_completo, 
        telefone, 
        email, 
        status_usuario, 
        cpf = None, 
        motivo_bloqueio=None,
        data_cadastro = None, 
        data_ultimo_acesso = None, 
        data_ultimo_servico = None,
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
            motivo_bloqueio=motivo_bloqueio,
            data_cadastro=data_cadastro,
            data_ultimo_acesso=data_ultimo_acesso, 
            foto_nome_usuario=foto_nome_usuario, 
            senha =senha, 
            id_usuario=id_usuario,
            endereco=endereco
            )

        self.__data_ultimo_servico = data_ultimo_servico

    @property
    def data_ultimo_servico(self):
        return self.__data_ultimo_servico

    @data_ultimo_servico.setter
    def data_ultimo_servico(self, value):
        self.__data_ultimo_servico = value



    