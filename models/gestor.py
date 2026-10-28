from datetime import datetime
from models.usuarios import Usuario


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

        self.fk_cnpj_barbearia = fk_cnpj_barbearia

    def consultarCnpjBarbearia(self):
        return self.fk_cnpj_barbearia

    def atualizarCnpjBarbearia(self, cnpj: str):
        self.fk_cnpj_barbearia = cnpj
