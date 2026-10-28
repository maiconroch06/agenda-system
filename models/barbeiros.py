from datetime import datetime
from models.usuarios import Usuario


class Barbeiro(Usuario):

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
        data_liberacao: datetime,
        descricao: str,
        status_barbeiro: bool,
        fk_id_agenda: int,
        fk_id_endereco: int = None
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

        self.data_liberacao = data_liberacao
        self.descricao = descricao
        self.status_barbeiro = status_barbeiro
        self.fk_id_agenda = fk_id_agenda

    def consultarDataLiberacao(self):
        return self.data_liberacao

    def atualizarDataLiberacao(self, data: datetime):
        self.data_liberacao = data

    def consultarDescricao(self):
        return self.descricao

    def atualizarDescricao(self, descricao: str):
        self.descricao = descricao

    def consultarStatusBarbeiro(self):
        return self.status_barbeiro

    def atualizarStatusBarbeiro(self, status: bool):
        self.status_barbeiro = status

    def consultarIdAgenda(self):
        return self.fk_id_agenda

    def atualizarIdAgenda(self, id_agenda: int):
        self.fk_id_agenda = id_agenda
