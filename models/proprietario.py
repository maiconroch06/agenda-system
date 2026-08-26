from .Users import Users

class proprietario(Users):
    def __init__(self, cpf, nome, sobrenome, telefone, email, senha, fotoPerfil, ativo, endereco):
        super().__init__(cpf, nome, sobrenome, telefone, email, senha, fotoPerfil, ativo, endereco)