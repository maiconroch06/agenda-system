class Endereco:

    def __init__(
        self,
        id: int,
        cep: str,
        cidade: str,
        estados_br_sigla: str,
        logradouro: str,
        numero: int,
        bairro: str,
        sequencia: int = None,
        complemento: str = None
    ):
        self.id = id
        self.cep = cep
        self.cidade = cidade
        self.estados_br_sigla = estados_br_sigla
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.sequencia = sequencia
        self.complemento = complemento

    def consultarCep(self):
        return self.cep

    def atualizarCep(self, cep: str):
        self.cep = cep

    def consultarCidade(self):
        return self.cidade

    def atualizarCidade(self, cidade: str):
        self.cidade = cidade

    def consultarEstado(self):
        return self.estados_br_sigla

    def atualizarEstado(self, estado: str):
        self.estados_br_sigla = estado

    def consultarLogradouro(self):
        return self.logradouro

    def atualizarLogradouro(self, logradouro: str):
        self.logradouro = logradouro

    def consultarNumero(self):
        return self.numero

    def atualizarNumero(self, numero: int):
        self.numero = numero

    def consultarBairro(self):
        return self.bairro

    def atualizarBairro(self, bairro: str):
        self.bairro = bairro

    def consultarSequencia(self):
        return self.sequencia

    def atualizarSequencia(self, sequencia: int):
        self.sequencia = sequencia

    def consultarComplemento(self):
        return self.complemento

    def atualizarComplemento(self, complemento: str):
        self.complemento = complemento

    def __str__(self):
        return (
            f"Endereco(id={self.id}, "
            f"cep='{self.cep}', "
            f"cidade='{self.cidade}', "
            f"estado='{self.estados_br_sigla}', "
            f"logradouro='{self.logradouro}', "
            f"numero={self.numero}, "
            f"bairro='{self.bairro}', "
            f"sequencia={self.sequencia}, "
            f"complemento='{self.complemento}')"
        )
