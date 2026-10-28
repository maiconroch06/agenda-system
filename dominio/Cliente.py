from Usuario import Usuario

class Cliente(Usuario):

    def __init__(
        self,
        id: int,
        nome: str,
        email: str,
        cpf: str,
        telefone: str,
        endereco: str
    ):
        # Inicializa os atributos da superclasse Usuario
        super().__init__(id, nome, email, cpf)

        # Atributos específicos da subclasse Cliente
        self.telefone = telefone
        self.endereco = endereco