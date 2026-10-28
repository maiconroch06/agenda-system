class Usuario:

    def __init__(self, id: int, nome: str, email: str, cpf: str):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf

    def validarCPF(self):
        return False if not self.cpf or not self.cpf.strip() else True