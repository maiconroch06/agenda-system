from datetime import datetime
from models.usuarios import Usuario

class Cliente(Usuario):

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
        fk_id_endereco: int = None,
        data_ultimo_servico: datetime = None
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
            fk_id_endereco=fk_id_endereco
        )

        self.data_ultimo_servico = data_ultimo_servico

    def consultarDataUltimoServico(self):
        return self.data_ultimo_servico

    def atualizarDataUltimoServico(self, data: datetime):
        self.data_ultimo_servico = data
