class Endereco:

    def __init__(
        self,
        cep: str,
        cidade: str,
        estados_br_sigla: str,
        logradouro: str,
        numero: int,
        bairro: str,
<<<<<<< HEAD
        id: int | None = None,
        sequencia: int = None,
        complemento: str = None
=======
        id = None,
        sequencia = None,
        complemento = None
>>>>>>> dev
    ):
        self.__id = id
        self.__cep = cep
        self.__cidade = cidade
        self.__estados_br_sigla = estados_br_sigla
        self.__logradouro = logradouro
        self.__numero = numero
        self.__bairro = bairro
        self.__sequencia = sequencia
        self.__complemento = complemento

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def cep(self):
        return self.__cep

    @cep.setter
    def cep(self, value):
        self.__cep = value

    @property
    def cidade(self):
        return self.__cidade

    @cidade.setter
    def cidade(self, value):
        self.__cidade = value

    @property
    def estados_br_sigla(self):
        return self.__estados_br_sigla

    @estados_br_sigla.setter
    def estados_br_sigla(self, value):
        self.__estados_br_sigla = value

    @property
    def logradouro(self):
        return self.__logradouro

    @logradouro.setter
    def logradouro(self, value):
        self.__logradouro = value

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, value):
        self.__numero = value

    @property
    def bairro(self):
        return self.__bairro

    @bairro.setter
    def bairro(self, value):
        self.__bairro = value

    @property
    def sequencia(self):
        return self.__sequencia

    @sequencia.setter
    def sequencia(self, value):
        self.__sequencia = value

    @property
    def complemento(self):
        return self.__complemento

    @complemento.setter
    def complemento(self, value):
        self.__complemento = value


   

    def _str__(self):
        return (
            f"Endereco(id={self.__id}, "
            f"cep='{self.__cep}', "
            f"cidade='{self.__cidade}', "
            f"estado='{self.__estados_br_sigla}', "
            f"logradouro='{self.__logradouro}', "
            f"numero={self.__numero}, "
            f"bairro='{self.__bairro}', "
            f"sequencia={self.__sequencia}, "
            f"complemento='{self.__complemento}')"
        )
