class Endereco:

    def __init__(
        self,
        cep: str,
        cidade: str,
        uf: str,
        logradouro: str,
        numero: int,
        bairro: str,
        id_endereco = None,
        sequencia = None,
        complemento = None
    ):
        self.__id_endereco = id_endereco
        self.__cep = cep
        self.__cidade = cidade
        self.__uf = uf
        self.__logradouro = logradouro
        self.__numero = numero
        self.__bairro = bairro
        self.__sequencia = sequencia
        self.__complemento = complemento

    @property
    def id_endereco(self):
        return self.__id_endereco

    @id_endereco.setter
    def id_endereco(self, value):
        self.__id_endereco = value

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
    def uf(self):
        return self.__uf

    @uf.setter
    def uf(self, value):
        self.__uf = value

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
            f"estado='{self.__uf}', "
            f"logradouro='{self.__logradouro}', "
            f"numero={self.__numero}, "
            f"bairro='{self.__bairro}', "
            f"sequencia={self.__sequencia}, "
            f"complemento='{self.__complemento}')"
        )
