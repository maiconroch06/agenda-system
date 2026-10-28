from datetime import datetime

class Usuario:

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
        fk_id_endereco: int = None
    ):
        self.id = id
        self.nome_completo = nome_completo
        self.telefone = telefone
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.foto_nome = foto_nome
        self.status_usuario = status_usuario
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao
        self.fk_id_endereco = fk_id_endereco

    def validarCPF(self):
        return bool(self.cpf and self.cpf.strip())

    def validarNome(self):
        return bool(self.nome_completo and self.nome_completo.strip())

    def validarEmail(self):
        return bool(self.email and self.email.strip())

    def validarTelefone(self):
        return bool(self.telefone and self.telefone.strip())

    def validarSenha(self):
        return bool(self.senha and self.senha.strip())

    def __str__(self):
        return f"Usuario(id={self.id}, nome={self.nome_completo})"